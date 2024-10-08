import unittest
import string
from _groupsig import ffi

from pygroupsig import groupsig
from pygroupsig import grpkey
from pygroupsig import mgrkey
from pygroupsig import memkey
from pygroupsig import signature
from pygroupsig import gml
from pygroupsig import constants


UINT_MAX = 2**32 - 1


# Parent class with common functions
class TestCommon(unittest.TestCase):

    # Non-test functions
    def addMember(self):
        msg1 = groupsig.join_mgr(0, self.isskey, self.grpkey, gml = self.gml)
        msg2 = groupsig.join_mem(1, self.grpkey, msgin = msg1)
        usk = msg2['memkey']
        msg3 = groupsig.join_mgr(2, self.isskey, self.grpkey, msg2['msgout'], gml = self.gml)
        msg4 = groupsig.join_mem(3, self.grpkey, msgin = msg3, memkey = usk)
        usk = msg4['memkey']
        self.memkeys.append(usk)

    def setUp(self):
        self.code = constants.KLAP20_CODE
        groupsig.init(self.code, 0)
        group1 = groupsig.setup(self.code)
        grpkey1 = group1['grpkey']
        self.isskey = group1['mgrkey']
        self.gml = group1['gml']
        group2 = groupsig.setup(self.code, grpkey1);
        self.opnkey = group2['mgrkey']
        self.grpkey = group2['grpkey']
        self.memkeys = []

    def tearDown(self):
        groupsig.clear(self.code)


# Tests for group operations
class TestGroupOps(TestCommon):

    # Creates a group
    def test_groupCreate(self):
        self.assertNotEqual(self.grpkey, ffi.NULL)
        self.assertNotEqual(self.isskey, ffi.NULL)
        self.assertNotEqual(self.opnkey, ffi.NULL)
        self.assertEqual(groupsig.get_joinseq(self.code), 3)
        self.assertEqual(groupsig.get_joinstart(self.code), 0)

    # Adds one member
    def test_addMember(self):
        n_members = len(self.memkeys)
        self.addMember()
        self.assertEqual(len(self.memkeys), n_members+1)
        self.assertNotEqual(self.memkeys[n_members], ffi.NULL)

    # Accepts a valid signature for a message passed as a string
    def test_acceptValidSignatureString(self):
        self.addMember()
        sig = groupsig.sign("Hello, World!", self.memkeys[0], self.grpkey, UINT_MAX)
        b = groupsig.verify(sig, "Hello, World!", self.grpkey)
        self.assertTrue(b)

    # Rejects a valid signature for a different message, also passed as a string
    def test_rejectValidSignatureWrongMessageString(self):
        self.addMember()
        sig = groupsig.sign("Hello, World!", self.memkeys[0], self.grpkey, UINT_MAX)
        b = groupsig.verify(sig, "Hello, Worlds!", self.grpkey)
        self.assertFalse(b)

    # Accepts a valid signature for a message passed as a byte array
    def test_acceptValidSignatureBytes(self):
        self.addMember()
        sig = groupsig.sign(b"Hello, World!", self.memkeys[0], self.grpkey, UINT_MAX)
        b = groupsig.verify(sig, b"Hello, World!", self.grpkey)
        self.assertTrue(b)

    # Rejects a valid signature for a different message, also passed as a byte array
    def test_rejectValidSignatureWrongMessageBytes(self):
        self.addMember()
        sig = groupsig.sign(b"Hello, World!", self.memkeys[0], self.grpkey, UINT_MAX)
        b = groupsig.verify(sig, b"Hello, Worlds!", self.grpkey)
        self.assertFalse(b)

    # Accepts a batch of valid signatures
    def test_acceptValidSignatureBatch(self):
        self.addMember()
        sigs = []
        msgs = []
        for i in range(10):
            msg = "Hello, World "+ str(i) + "!"
            sig = groupsig.sign(msg, self.memkeys[0], self.grpkey, UINT_MAX)
            msgs.append(msg)
            sigs.append(sig)
        b = groupsig.verify_batch(sigs, msgs, self.grpkey)
        self.assertTrue(b)

    # Reject a batch of signatures including a wrong signature
    def test_rejectWrongSignatureBatch(self):
        self.addMember()
        sigs = []
        msgs = []
        for i in range(10):
            msg = "Hello, World "+ str(i) + "!"
            sig = groupsig.sign(msg, self.memkeys[0], self.grpkey, UINT_MAX)
            msgs.append(msg)
            sigs.append(sig)
        msgs[0] = "Hello, World!"
        b = groupsig.verify_batch(sigs, msgs, self.grpkey)
        self.assertFalse(b)

    # Successfully opens a signature
    def test_openSignature(self):
        self.addMember()
        self.addMember()
        sig = groupsig.sign(b"Hello, World!", self.memkeys[1], self.grpkey, UINT_MAX)
        gsopen = groupsig.open(sig, self.opnkey, self.grpkey, gml = self.gml)
        self.assertEqual(gsopen["index"], 1)
        proof = gsopen['proof']
        b = groupsig.open_verify(proof, sig, self.grpkey)
        self.assertTrue(b)


# Tests for signature operations
class TestSignatureOps(TestCommon):

    # Creates a group, adds a member and generates a signature
    def setUp(self):
        super().setUp()
        self.addMember()
        self.sig = groupsig.sign("Hello, World!", self.memkeys[0], self.grpkey, UINT_MAX)

    # Exports and reimports a signature, and it verifies correctly
    def test_sigExportImport(self):
        sig_str = signature.signature_export(self.sig)
        sig = signature.signature_import(self.code, sig_str)
        b = groupsig.verify(sig, "Hello, World!", self.grpkey)
        self.assertTrue(b)

    # Prints a string (this just checks the produced string is not empty)
    def test_sigToString(self):
        sig_str = signature.signature_to_string(self.sig)
        self.assertGreater(len(sig_str), 0)
        self.assertTrue(set(sig_str).issubset(set(string.printable)))


# Tests for group key operations
class TestGrpkeyOps(TestCommon):

    # Exports and reimports a group key
    def test_grpkeyExportImport(self):
        grpkey_str = grpkey.grpkey_export(self.grpkey)
        gpk = grpkey.grpkey_import(self.code, grpkey_str)
        # This is quite useless, as import returns an exception if the FFI
        # method returns ffi.NULL. Maybe implementing a cmp function for
        # grp keys would be good for testing this (and also in general?)
        self.assertIsNot(ffi.NULL, gpk)


# Tests for manager key operations
class TestIssuerkeyOps(TestCommon):

    # Exports and reimports an manager key
    def test_isskeyExportImport(self):
        isskey_str = mgrkey.mgrkey_export(self.isskey)
        ikey = mgrkey.mgrkey_import(self.code, isskey_str)
        # This is quite useless, as import returns an exception if the FFI
        # method returns ffi.NULL. Maybe implementing a cmp function for
        # manager keys would be good for testing this (and also in general?)
        self.assertIsNot(ffi.NULL, ikey)


# Tests for opener key operations
class TestOpenerkeyOps(TestCommon):

    # Exports and reimports a converter key
    def test_opnkeyExportImport(self):
        opnkey_str = mgrkey.mgrkey_export(self.opnkey)
        okey = mgrkey.mgrkey_import(self.code, opnkey_str)
        # This is quite useless, as import returns an exception if the FFI
        # method returns ffi.NULL. Maybe implementing a cmp function for
        # manager keys would be good for testing this (and also in general?)
        self.assertIsNot(ffi.NULL, okey)


# Tests for member key operations
class TestMemkeyOps(TestCommon):

    # Exports and reimports a member key
    def test_memkeyExportImport(self):
        self.addMember()
        memkey_str = memkey.memkey_export(self.memkeys[0])
        mkey = memkey.memkey_import(self.code, memkey_str)
        # This is quite useless, as import returns an exception if the FFI
        # method returns ffi.NULL. Maybe implementing a cmp function for
        # mem keys would be good for testing this (and also in general?)
        self.assertIsNot(ffi.NULL, mkey)


# Tests for GML operations
class TestGmlOps(TestCommon):

    # Exports and reimports a member key
    def test_gmlExportImport(self):
        self.addMember()
        self.addMember()
        self.addMember()
        gml_str = gml.gml_export(self.gml)
        _gml = gml.gml_import(self.code, gml_str)
        # This is quite useless, as import returns an exception if the FFI
        # method returns ffi.NULL. Maybe implementing a cmp function for
        # GMLs would be good for testing this (and also in general?)
        self.assertIsNot(ffi.NULL, _gml)


# Define test suites
def suiteGroupOps():
    suiteGroupOps = unittest.TestSuite()
    suiteGroupOps.addTest(TestGroupOps('test_groupCreate'))
    suiteGroupOps.addTest(TestGroupOps('test_addMember'))
    suiteGroupOps.addTest(TestGroupOps('test_acceptValidSignatureString'))
    suiteGroupOps.addTest(TestGroupOps('test_rejectValidSignatureWrongMessageString'))
    suiteGroupOps.addTest(TestGroupOps('test_acceptValidSignatureBytes'))
    suiteGroupOps.addTest(TestGroupOps('test_rejectValidSignatureWrongMessageBytes'))
    suiteGroupOps.addTest(TestGroupOps('test_acceptValidSignatureBatch'))
    suiteGroupOps.addTest(TestGroupOps('test_rejectWrongSignatureBatch'))
    suiteGroupOps.addTest(TestGroupOps('test_openSignature'))
    return suiteGroupOps


def suiteSigOps():
    suiteSigOps = unittest.TestSuite()
    suiteSigOps.addTest(TestSignatureOps('test_sigExportImport'))
    suiteSigOps.addTest(TestSignatureOps('test_sigToString'))
    return suiteSigOps


def suiteGrpkeyOps():
    suiteGrpkeyOps = unittest.TestSuite()
    suiteGrpkeyOps.addTest(TestGrpkeyOps('test_grpkeyExportImport'))
    return suiteGrpkeyOps


def suiteIssuerkeyOps():
    suiteIssuerkeyOps = unittest.TestSuite()
    suiteIssuerkeyOps.addTest(TestIssuerkeyOps('test_isskeyExportImport'))
    return suiteIssuerkeyOps


def suiteOpenerkeyOps():
    suiteOpenerkeyOps = unittest.TestSuite()
    suiteOpenerkeyOps.addTest(TestOpenerkeyOps('test_opnkeyExportImport'))
    return suiteOpenerkeyOps


def suiteMemkeyOps():
    suiteMemkeyOps = unittest.TestSuite()
    suiteMemkeyOps.addTest(TestMemkeyOps('test_memkeyExportImport'))
    return suiteMemkeyOps


def suiteGmlOps():
    suiteGmlOps = unittest.TestSuite()
    suiteGmlOps.addTest(TestGmlOps('test_gmlExportImport'))
    return suiteGmlOps


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suiteGroupOps())
    runner.run(suiteSigOps())
    runner.run(suiteGrpkeyOps())
    runner.run(suiteIssuerkeyOps())
    runner.run(suiteOpenerkeyOps())
    runner.run(suiteMemkeyOps())
    runner.run(suiteGmlOps())
