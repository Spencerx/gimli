#!/usr/bin/env python
"""
Basic tests
"""
import unittest
import time

import numpy as np
import pygimli as pg


class ModellingMT(pg.ModellingBase):
    def __init__(self, nPars, verbose):
        """ """
        pg.ModellingBase.__init__(self, verbose)
        self.regionManager().setParameterCount(nPars)

    def response(self, par):
        """ """
        return par * 1.0

    def response_mt(self, par, i=0):
        """ """
        time.sleep(0.1)
        # print(i)
        return par * 2.0


class TestFOP(unittest.TestCase):

    def test_FOP(self):
        """ Test FOP """
        # ab2 = pg.RVector(2, 1.0)
        # ab2[1] = 2.0
        # mn2 = pg.RVector(2, 3.0)
        # mn2[1] = 4.0

        # nlay = 2
        # model = pg.RVector(3, 10.)

        # F = pg.DC1dModelling(nlay, ab2, mn2)

        # print(F.response(model))

        pass

    def test_multiResponseMT(self):
        """ Test FOP response - mt"""
        nPars = 4
        m = pg.RVector(nPars, 1)
        fop = ModellingMT(nPars, verbose=True)

        ms = np.array([m*2, m*3, m*4, m*5])
        fop.setMultiThreadJacobian(1)
        ds1 = np.zeros((len(ms), len(ms[0])))
        fop.responses(ms, ds1)

        fop.setMultiThreadJacobian(4)
        ds2 = np.zeros((len(ms), len(ms[0])))
        fop.responses(ms, ds2)

        np.testing.assert_array_equal(ds1, ds2)

    def test_MT(self):
        """ """
        nPars = 4
        m = pg.RVector(nPars, 1)

        fop = ModellingMT(nPars, verbose=False)
        fop.setMultiThreadJacobian(1)
        fop.createJacobian(m)
        J1 = pg.RMatrix(fop.jacobian())

        fop.setMultiThreadJacobian(4)
        fop.createJacobian(m)
        J2 = fop.jacobian()

        np.testing.assert_array_equal(J1 * 2.0, J2)

        # for i in range(J1.rows()):
        #   print(np.array(J1[i]), np.array(J2[i]))
        #   np.testing.assert_array_equal(np.array(J1[i]), np.array(J2[i]))


if __name__ == '__main__':

    unittest.main()
