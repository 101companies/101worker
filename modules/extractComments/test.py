from .program import run, getLanguages
import unittest
from unittest.mock import Mock, patch


class ExtractCommentsTest(unittest.TestCase):

    #Test for Java Single Line Comments
    def test_Java_singleCommentStandard(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.any'
        }
        sourceCode = "this is the regular \n code of a program \n which does something"
        commentText = "this is a comment"
        sourceCode = sourceCode + "\n "+"//"+commentText+"\n more code"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Java"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[commentText]}, 'comments')

    #Test for Java Multiline Comments
    def test_Java_multiCommentStandard(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.any'
        }
        sourceCode = "this is the regular \n code of a program \n which does something"
        commentText = "this is a comment"
        sourceCode = sourceCode + "\n "+"/*"+commentText+"*/"+"more code"
        self.env = Mock()
        self.env.get_derived_resource.return_value = "Java"
        self.env.get_primary_resource.return_value = sourceCode
        run(self.env, change)
        self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[commentText]}, 'comments')


    #Test ALL entries in the language datastructure of .program
    def test_ALL_singleCommentStandard(self):
        languages = getLanguages()
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.any'
        }
        for key in languages.keys():
            sourceCode = "this is the regular \n code of a program \n which does something"
            lang = key
            singleComment = languages[key].get("Single")
            if singleComment != None:
                for comment in singleComment:
                    commentText = "this is a comment"
                    sourceCode = sourceCode + "\n "+comment+commentText+"\n more code"  
            else:
                    sourceCode = ""
                    commentText = ""
            self.env = Mock()
            self.env.get_derived_resource.return_value = key
            self.env.get_primary_resource.return_value = sourceCode
            run(self.env, change)
            self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[commentText]}, 'comments')
   
    #Test ALL entries in the language datastructure of .program
    def test_ALL_skipBlockInSingleLine(self):
        languages = getLanguages()
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.any'
        }
        for key in languages.keys():
            sourceCode = "this is the regular \n code of a program \n which does something"
            lang = key
            singleComment = languages[key].get("Single")
            if singleComment != None:
                if languages[key].get("Block") != None and languages[key].get("Block") != []:
                    blockStart = languages[key].get("Block")[0].get("BlockStart")
                    blockEnd = languages[key].get("Block")[0].get("BlockEnd")
                for comment in singleComment:
                    if languages[key].get("Block") != None and languages[key].get("Block") != []:
                        blockStart = languages[key].get("Block")[0].get("BlockStart")
                        blockEnd = languages[key].get("Block")[0].get("BlockEnd")
                        commentText = "this is a comment"+blockStart+"inside"+blockEnd
                    else:
                        commentText = "this is a comment"
                    sourceCode = sourceCode + "\n "+comment+commentText+"\n more code"  
            else:
                commentText = ""
                sourceCode = ""

            self.env = Mock()
            self.env.get_derived_resource.return_value = key
            self.env.get_primary_resource.return_value = sourceCode
            run(self.env, change)
            self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':[commentText]}, 'comments')
 
    #Test ALL entries in the language datastructure of .program
    def test_ALL_MultiLineCommentAlone(self):
        languages = getLanguages()
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.any'
        }
        
        for key in languages.keys():
            allComments = []
            sourceCode = "this is the regular \n code of a program \n which does something"
            lang = key
            if languages[key].get("Block") != None and languages[key].get("Block") != []:
                for blocksymbols in languages[key].get("Block"):
                    blockStart = blocksymbols.get("BlockStart")
                    blockEnd = blocksymbols.get("BlockEnd")
                    commentText = "Block Comment 1 starting and ending in own line(s)"
                    sourceCode = sourceCode + "\n "+blockStart+commentText+blockEnd+"\n more code"  
                    allComments.append(commentText)
                    commentText = "Block Comment 2 ending in line with code"
                    sourceCode = sourceCode + "\n "+blockStart+commentText+blockEnd+" more code"  
                    allComments.append(commentText)
            else:
                allComments = []
                sourceCode = ""

            self.env = Mock()
            self.env.get_derived_resource.return_value = key
            self.env.get_primary_resource.return_value = sourceCode
            run(self.env, change)
            self.env.write_derived_resource.assert_called_with('some-file.any', {'comments':allComments}, 'comments')


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(ExtractCommentsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
