__author__ = 'quentin'


import unittest
import time
import shutil
import random
import tempfile
from pysolovideo.tracking.roi_builders import ROI
from pysolovideo.utils.io import ResultWriter, SQLiteResultWriter


from pysolovideo.tracking.trackers import DataPoint, BoolVariableBase, IntVariableBase, DistanceIntVarBase
import logging
import numpy as np

np.random.seed(1)

class DummyBoolVariable(BoolVariableBase):
    header_name="dummy_bool"

class DummyIntVariable(IntVariableBase):
    functional_type = "dum_type"
    header_name="dummy_int"

class DummyDistVariable(DistanceIntVarBase):
    header_name="dummy_dist_int"

class XVar(DistanceIntVarBase):
    header_name="x"

class YVar(DistanceIntVarBase):
    header_name="y"

class RandomResultGenerator(object):
    def make_one_point(self):

        out = DataPoint([
                DummyBoolVariable(bool(int(random.uniform(0,2)))),
                DummyIntVariable(random.uniform(0,1000)),
                DummyDistVariable(random.uniform(0,1000)),
                XVar(random.uniform(0,1000)),
                YVar(random.uniform(0,1000)),
                ])
        return out


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    def test_dbwriter(RWClass, *args, **kwargs):

        # building five rois
        coordinates = np.array([(0,0), (100,0), (100,100), (0,100)])
        rois = [ROI(coordinates +i*100) for i in range(1,33)]
        rpg = RandomResultGenerator()

        with RWClass(None, rois=rois, *args, **kwargs) as rw:
            # n = 4000000 # 222h of data
            # n = 400000 # 22.2h of data
            n = 4000 # 2.22h of data
            import time
            t0 = time.time()
            try:
                t = 0
                while t < n:
                    t+=1


                    rt = time.time() * 1000
                    if t % (n/100)== 0:
                        logging.info("filling with dummy variables: %f percent" % (100.*float(t)/float(n)))
                    for r in rois:
                        data = rpg.make_one_point()
                        rw.write(rt , r, data)

                    rw.flush()
                    #
                    # if t % 100 == 0:
                    #     print t, flushed, time.time() - t0
                print "OK"

            except KeyboardInterrupt:
                return
        print "OK"

    test_dbwriter(ResultWriter, db_name="psv_test_io")


