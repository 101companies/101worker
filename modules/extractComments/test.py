from .program import run, getLanguages
import unittest
from unittest.mock import Mock, patch


class ExtractCommentsTest(unittest.TestCase):
  
    def setUp(self):
        self.change = {
            'type': 'NEW_FILE',
            'file': 'some-file.any'
        }        
        self.commentText = "a great comment"

    #Test for Java Single Line Comments
    def test_Java_singleCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"//"+self.commentText+"\n"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Java"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Java Multiline Comments
    def test_Java_multiCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"/*"+self.commentText+"*/"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Java"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Java SingleLine including multiLine Begin
    def test_Java_singleMultiCommentExt(self):
        sourceCode = "x=42 \n y=101 \n "+"//"+self.commentText+"/* abc\n"+"z=x+y \n"+"x=42 \n y=101 \n "+"/*"+self.commentText+"*/"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Java"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText+"/* abc",self.commentText]}, 'comments')

    #Test for Haskell Single Line Comments
    def test_Haskell_singleCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"--"+self.commentText+"\n"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Haskell"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Haskell Multiline Comments
    def test_Haskell_multiCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"{-"+self.commentText+"-}"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Haskell"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Haskell SingleLine including multiLine Begin
    def test_Haskell_singleMultiCommentExt(self):
        sourceCode = "x=42 \n y=101 \n "+"--"+self.commentText+"{- abc\n"+"z=x+y \n"+"x=42 \n y=101 \n "+"{-"+self.commentText+"-}"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Haskell"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText+"{- abc",self.commentText]}, 'comments')


    #Test for Python Single Line Comments
    def test_Python_singleCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"#"+self.commentText+"\n"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Python"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Python Multiline Comments1
    def test_Python_multiCommentStandard1(self):
        sourceCode = "x=42 \n y=101 \n "+"'''"+self.commentText+"'''"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Python"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Python Multiline Comments2
    def test_Python_multiCommentStandard2(self):
        sourceCode = "x=42 \n y=101 \n "+"\"\"\""+self.commentText+"\"\"\""+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Python"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Python SingleLine including multiLine Begin
    def test_Python_singleMultiCommentExt(self):
        sourceCode = "x=42 \n y=101 \n "+"#"+self.commentText+"''' abc\n"+"z=x+y \n"+"x=42 \n y=101 \n "+"'''"+self.commentText+"'''"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Python"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText+"''' abc",self.commentText]}, 'comments')

    #Test for Ruby Single Line Comments
    def test_Java_singleCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"#"+self.commentText+"\n"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Ruby"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for Ruby Multiline Comments
    def test_Java_multiCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"=begin"+self.commentText+"=end"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Ruby"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')
    
    #Test for C++ Single Line Comments
    def test_Java_singleCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"//"+self.commentText+"\n"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "CPlusPlus"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

    #Test for C++ Multiline Comments
    def test_Java_multiCommentStandard(self):
        sourceCode = "x=42 \n y=101 \n "+"/*"+self.commentText+"*/"+"z=x+y"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "CPlusPlus"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, self.change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[self.commentText]}, 'comments')

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(ExtractCommentsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

 
