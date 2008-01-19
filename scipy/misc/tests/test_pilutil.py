import os.path
import glob
import numpy as N

from scipy.testing import *

try:
    import PIL.Image
except ImportError:
    _have_PIL = False
else:
    _have_PIL = True
    import scipy.misc.pilutil as pilutil
TestCase.__test__ = _have_PIL

datapath = os.path.dirname(__file__)

class TestPILUtil(TestCase):
    def test_imresize(self):
        im = N.random.random((10,20))
        for T in N.sctypes['float'] + [float]:
            im1 = pilutil.imresize(im,T(1.1))
            assert_equal(im1.shape,(11,22))

    def test_bytescale(self):
        x = N.array([0,1,2],N.uint8)
        y = N.array([0,1,2])
        assert_equal(pilutil.bytescale(x),x)
        assert_equal(pilutil.bytescale(y),[0,127,255])


def tst_fromimage(filename, irange):
    img = pilutil.fromimage(PIL.Image.open(filename))
    imin,imax = irange
    assert img.min() >= imin
    assert img.max() <= imax

@dec.setastest(_have_PIL)
def test_fromimage():
    ''' Test generator for parametric tests '''
    data = {'icon.png':(0,255),
            'icon_mono.png':(0,2),
            'icon_mono_flat.png':(0,1)}
    for fn, irange in data.iteritems():
        yield tst_fromimage, os.path.join(datapath,'data',fn), irange

if __name__ == "__main__":
    nose.run(argv=['', __file__])
