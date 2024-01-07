# copy the files empty.txt and sample.txt from the source package
# into the /tmp folder before running this test.

import unittest

from other_progs.wc import WordCount, ContentAnalysis


class TestWordCount(unittest.TestCase):
    def test_word_count_on_a_non_existent_file_returns_None(self):
        wc = WordCount()
        analysis = wc.analyze_file(None)
        self.assertIsNone(analysis)

    def test_word_count_on_an_empty_file_returns_zero_result(self):
        wc = WordCount()
        analysis = wc.analyze_file('/tmp/empty.txt')
        self.assertIsNotNone(analysis)
        self.assertEqual(type(analysis), ContentAnalysis)
        self.assertEqual(analysis.total_word_count, 0)
        self.assertEqual(analysis.line_count, 0)
        self.assertEqual(analysis.char_count, 0)
        self.assertEqual(analysis.unique_word_count, 0)
        self.assertEqual(analysis.white_space_count, 0)

    def test_word_count_on_a_valid_file_produces_non_zero_results(self):
        wc = WordCount()
        analysis = wc.analyze_file('/tmp/sample.txt')
        self.assertIsNotNone(analysis)
        # print(analysis.content)
        self.assertEqual(type(analysis), ContentAnalysis)
        self.assertEqual(analysis.line_count, 11)
        self.assertEqual(analysis.blank_line_count, 5)
        self.assertEqual(analysis.unique_word_count, 21)
        self.assertEqual(analysis.total_word_count, 33)
        self.assertEqual(analysis.char_count, 126)
