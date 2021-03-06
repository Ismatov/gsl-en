import unittest
import pexif
import StringIO
import difflib

try:
    import decimal
except:
    decimal = None

test_data = [
    ("test/data/rose.jpg", "test/data/rose.txt"),
    ("test/data/conker.jpg", "test/data/conker.txt"),
    ("test/data/noexif.jpg", "test/data/noexif.txt"),
    ]

DEFAULT_TESTFILE = test_data[0][0]
NONEXIST_TESTFILE = "test/data/noexif.jpg"

class TestMakeSyms(unittest.TestCase):
    set = {1 : ("one", 1), 2 : ("two", 2), 3 : ("three", 3), 4 : ("four", 4) }

    def setUp(self):
        pexif.make_syms(self.set)

    def test_basic(self):
        for num in [pexif.ONE, pexif.TWO, pexif.THREE, pexif.FOUR]:
            self.assertEqual(self.set[num][1], num)
        
    def tearDown(self):
        # Ideally remove symbols ... but can't think of a good way to do it
        pass

class TestLoadFunctions(unittest.TestCase):
    def test_fromFile(self):
        # Simple test ensures we can load and parse a file from filename
        for test_file, _ in test_data:
            pexif.JpegFile.fromFile(test_file)

    def test_fromString(self):
        # Simple test ensures we can load and parse a file passed as a string
        for test_file, _ in test_data:
            fd = open(test_file, "rb")
            data = fd.read()
            fd.close()
            pexif.JpegFile.fromString(data)

    def test_fromFd(self):
        # Simple test ensure we can load and parse a file passed as a fd
        for test_file, _ in test_data:
            fd = open(test_file, "rb")
            pexif.JpegFile.fromFd(fd)

    def test_emptyData(self):
        # Simple test ensures that empty string fails
        self.assertRaises(pexif.JpegFile.InvalidFile, pexif.JpegFile.fromString, "")

    def test_badData(self):
        # Simple test ensures that random crap doesn't get parsed
        self.assertRaises(pexif.JpegFile.InvalidFile, pexif.JpegFile.fromString,
                          "asl;dkfjasl;kdjfsld")

    def test_regen(self):
        # Test to ensure the new file matches the existing file
        for test_file, _ in test_data:
            data = open(test_file, "rb").read()
            jpeg = pexif.JpegFile.fromString(data)
            new_data = jpeg.writeString()
            self.assertEqual(data, new_data, "Binary differs for <%s>" % test_file)

    def test_dump(self):
        # Test that the dumped data is as expected.
        for test_file, expected_file in test_data:
            expected = open(expected_file).read()
            jpeg = pexif.JpegFile.fromFile(test_file)
            out = StringIO.StringIO()
            jpeg.dump(out)
            res = "Error in file <%s>\n" % test_file
            x = difflib.unified_diff(expected.split('\n'), out.getvalue().split('\n'))
            for each in x:
                res += each
                res += '\n'
            self.assertEqual(expected, out.getvalue(), res)

class TestExifFunctions(unittest.TestCase):
    def test_badexif(self):
        data = list(open(DEFAULT_TESTFILE, "rb").read())
        # Now trash the exif signature
        assert(data[0x18] == 'E')
        data[0x18] = 'F'

        self.assertRaises(pexif.JpegFile.InvalidFile, pexif.JpegFile.fromString, "".join(data))

    def test_badendian(self):
        data = list(open(DEFAULT_TESTFILE, "rb").read())
        # Now trash the exif signature
        assert(data[0x1E] == 'I')
        data[0x1E] = '0'
        self.assertRaises(pexif.JpegFile.InvalidFile, pexif.JpegFile.fromString, "".join(data))

    def test_badtifftag(self):
        data = list(open(DEFAULT_TESTFILE, "rb").read())
        # Now trash the exif signature
        assert(data[0x20] == '\x2a')
        data[0x20] = '0'
        self.assertRaises(pexif.JpegFile.InvalidFile, pexif.JpegFile.fromString, "".join(data))

    def test_goodexif(self):
        for test_file, _ in test_data:
            jp = pexif.JpegFile.fromFile(test_file)
            jp.get_exif()

    def test_noexif(self):
        jp = pexif.JpegFile.fromFile(NONEXIST_TESTFILE)
        self.assertEqual(jp.get_exif(), None)

    def test_noexif_create(self):
        jp = pexif.JpegFile.fromFile(NONEXIST_TESTFILE)
        self.assertNotEqual(jp.get_exif(create=True), None)

    def test_getattr_nonexist(self):
        for test_file, _ in test_data:
            attr = pexif.JpegFile.fromFile(test_file). \
                   get_exif(create=True). \
                   get_primary(create=True)
            self.assertEqual(attr[pexif.ImageWidth], None)

    def test_getattr_exist(self):
        attr = pexif.JpegFile.fromFile(DEFAULT_TESTFILE).get_exif().get_primary()
        self.assertEqual(attr[pexif.Make], "Canon")

    def test_setattr_nonexist(self):
        for test_file, _ in test_data:
            attr = pexif.JpegFile.fromFile(test_file). \
                   get_exif(create=True).get_primary(create=True)
            attr[pexif.ImageWidth] = 3
            self.assertEqual(attr[pexif.ImageWidth], 3)

    def test_setattr_exist(self):
        for test_file, _ in test_data:
            attr = pexif.JpegFile.fromFile(test_file). \
                   get_exif(create=True). \
                   get_primary(create=True)
            attr[pexif.Make] = "CanonFoo"
            self.assertEqual(attr[pexif.Make], "CanonFoo")
        
    def test_setattr_exist_none(self):
        for test_file, _ in test_data:
            attr = pexif.JpegFile.fromFile(test_file). \
                   get_exif(create=True). \
                   get_primary(create=True)
            attr[pexif.Make] = None
            self.assertEqual(attr[pexif.Make], None)

    def test_add_geo(self):
        for test_file, _ in test_data:
            jf = pexif.JpegFile.fromFile(test_file)
            try:
                jf.get_geo()
                return
            except jf.NoSection:
                pass
            attr = jf.get_exif(create=True).get_primary(create=True)
            gps = attr.new_gps()
            gps[pexif.GPSLatitudeRef] = "S"
            gps[pexif.GPSLongitudeRef] = "E"
            data = jf.writeString()
            jf2 = pexif.JpegFile.fromString(data)
            self.assertEqual(jf2.get_exif().get_primary() \
                             [pexif.GPSIFD][pexif.GPSLatitudeRef], "S")

    def test_simple_add_geo(self):
        for test_file, _ in test_data:
            jf = pexif.JpegFile.fromFile(test_file)
            (lat, lng) = (-37.312312, 45.412321)
            jf.set_geo(lat, lng)
            new_file = jf.writeString()
            new = pexif.JpegFile.fromString(new_file)
            new_lat, new_lng = new.get_geo()
            self.assertAlmostEqual(lat, new_lat, 6)
            self.assertAlmostEqual(lng, new_lng, 6)

    def test_simple_add_geo2(self):
        for test_file, _ in test_data:
            jf = pexif.JpegFile.fromFile(test_file)
            (lat, lng) = (51.522, -1.455)
            jf.set_geo(lat, lng)
            new_file = jf.writeString()
            new = pexif.JpegFile.fromString(new_file)
            new_lat, new_lng = new.get_geo()
            self.assertAlmostEqual(lat, new_lat, 6)
            self.assertAlmostEqual(lng, new_lng, 6)

    def test_simple_add_geo3(self):
        for test_file, _ in test_data:
            jf = pexif.JpegFile.fromFile(test_file)
            (lat, lng) = (51.522, -1.2711)
            jf.set_geo(lat, lng)
            new_file = jf.writeString()
            new = pexif.JpegFile.fromString(new_file)
            new_lat, new_lng = new.get_geo()
            self.assertAlmostEqual(lat, new_lat, 6)
            self.assertAlmostEqual(lng, new_lng, 6)

    def test_get_geo(self):
        jf = pexif.JpegFile.fromFile(DEFAULT_TESTFILE)
        self.assertRaises(pexif.JpegFile.NoSection, jf.get_geo)

if __name__ == "__main__":
    unittest.main()
