from sprokit.pipeline import process
from kwiver.kwiver_process import KwiverProcess
from vital.types import Image
from vital.types import ImageContainer
from vital.types import DetectedObject
from vital.types import DetectedObjectSet
from vital.types import BoundingBox

import tensorflow as tf
import numpy as np
import humanfriendly
import time
import os

from PIL import Image
from vital.util.VitalPIL import get_pil_image


class tf_detector(KwiverProcess):
    """
    This process gets an image as input, does some stuff to it and
    sends the modified version to the output port.
    """
    # ----------------------------------------------

    def __init__(self, conf):
        print( "[DEBUG] ----- init" )
        KwiverProcess.__init__(self, conf)

        self.add_config_trait("modelFile", "modelFile", 'Model File',
          'Path to TF Inference Graph.')

        self.declare_config_using_trait('modelFile')

        self.add_port_trait('out_image', 'image', 'Processed image')

        # set up required flags
        optional = process.PortFlags()
        required = process.PortFlags()
        required.add(self.flag_required)

        #  declare our input port ( port-name,flags)
        self.declare_input_port_using_trait('image', required)
        self.declare_output_port_using_trait('detected_object_set', optional)

        self.confidenceThresh = .5

    def __del__(self):
        print( "[DEBUG] ----- close" )
        self.sess.close()

    # ----------------------------------------------
    def _configure(self):
        print( "[DEBUG] ----- configure" )
        self.modelFile = self.config_value('modelFile')

        # Load and detector
        self.detection_graph = self.load_model(self.modelFile)

        self.sess = tf.Session(graph=self.detection_graph)

        self._base_configure()

    # ----------------------------------------------
    def _step(self):
        print( "[DEBUG] ----- start step" )
        # grab image container from port using traits
        in_img_c = self.grab_input_using_trait('image')

        # Get python image from conatiner (just for show)
        in_img = np.array(get_pil_image(in_img_c.image()).convert('RGB'))

        s = in_img.shape; imageHeight = s[0]; imageWidth = s[1]

        startTime = time.time()
        boxes, scores, classes = self.generate_detection(self.detection_graph, in_img)
        elapsed = time.time() - startTime
        print("Done running detector in {}".format(humanfriendly.format_timespan(elapsed)))

        goodBoxes = []
        detections = DetectedObjectSet()

        for i in range(0, len(scores)):
           if(scores[i] >= self.confidenceThresh):
               bbox = boxes[i]
               goodBoxes.append(bbox)

               topRel = bbox[0]
               leftRel = bbox[1]
               bottomRel = bbox[2]
               rightRel = bbox[3]
            
               xmin = leftRel * imageWidth
               ymin = topRel * imageHeight
               xmax = rightRel * imageWidth
               ymax = bottomRel * imageHeight

               obj = DetectedObject(BoundingBox(xmin, ymin, xmax, ymax), scores[i])
               detections.add(obj)

        print("Detected {}".format(len(goodBoxes)))

        self.push_to_port_using_trait('detected_object_set', detections)

        self._base_step()

    def load_model(self, checkpoint):
        """
        Load a detection model (i.e., create a graph) from a .pb file
        """

        print('Creating Graph...')
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(checkpoint, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        print('...done')

        return detection_graph

    def generate_detection(self, detection_graph, imageNP):
        """
        boxes,scores,classes,images = generate_detection(detection_graph,image)

        Run an already-loaded detector network on an image.

        Boxes are returned in relative coordinates as (top, left, bottom, right); x,y origin is the upper-left.
        """

        imageNP_expanded = np.expand_dims(imageNP, axis=0)
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        box = detection_graph.get_tensor_by_name('detection_boxes:0')
        score = detection_graph.get_tensor_by_name('detection_scores:0')
        clss = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # Actual detection
        (box, score, clss, num_detections) = self.sess.run(
            [box, score, clss, num_detections],
            feed_dict={image_tensor: imageNP_expanded})

        boxes = np.squeeze(np.array(box))
        scores = np.squeeze(np.array(score))
        classes = np.squeeze(np.array(clss)).astype(int)

        return boxes, scores, classes
