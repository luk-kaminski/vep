#!/usr/bin/env python3

import unittest
import numpy as np
import numpy.testing as npt
import src.vector_tools as vt


class TestVectorTools(unittest.TestCase):

    def test_normalize(self):
        npt.assert_array_equal(np.array([0, 1]), vt.normalize(np.array([0, 2])))
        npt.assert_array_equal(np.array([0.6, 0.8]), vt.normalize(np.array([3, 4])))

    def test_similarity(self):
        self.assertEqual(1.0, vt.similarity([1, 2, 3, 4], [1, 2, 3, 4]))  # same vectors
        self.assertEqual(0.0, vt.similarity([1, 0, 3, 0], [0, 2, 0, 4]))  # orthogonal vectors
        self.assertEqual(-1.0, vt.similarity([1, 2, 3, 4], [-1, -2, -3, -4]))  # negated vectors

    def test_vector_add_and_retrieve(self):
        sut = vt.NamedVectors(3)
        sut.add_vector('name', np.array([0, 3, 1]))

        npt.assert_array_equal(np.array([0, 3, 1]), sut.get_vector('name'))
        self.assertIsNone(sut.get_vector('missing'))

    def test_to_matrix(self):
        sut = vt.NamedVectors(3)
        sut.add_vector('zero', np.array([0, 0, 0]))
        sut.add_vector('one', np.array([1, 1, 1]))
        sut.add_vector('two', np.array([2, 2, 2]))
        sut.add_vector('mixed', np.array([7, 1, 7]))

        matrix = sut.to_matrix(['zero', 'mixed', 'two', 'one'])
        expected = np.array([[0, 0, 0], [7, 1, 7], [2, 2, 2], [1, 1, 1]])
        npt.assert_array_equal(expected, matrix)

    def test_throws_exception_when_vector_of_wrong_size_added(self):
        sut = vt.NamedVectors(5)
        with self.assertRaises(ValueError):
            sut.add_vector('name', np.array([0, 3, 1]))

    def test_find_synonyms(self):
        sut = vt.NamedVectors(3)
        sut.add_vector('money', np.array([0, 0, 3]))
        sut.add_vector('cash', np.array([0.2, 0.3, 2.5]))
        sut.add_vector('currency', np.array([0.5, 0.7, 1.5]))

        perfect_synonyms = sut.find_synonyms([0, 0, 3], 0.99)
        self.assertEqual(1, len(perfect_synonyms))
        self.assertEqual('money', perfect_synonyms[0][0])
        self.assertTrue(perfect_synonyms[0][1] >= 0.99)

        close_similarity = 0.98
        close_synonyms = sut.find_synonyms([0, 0, 3], close_similarity)
        self.assertEqual(2, len(close_synonyms))
        self.assertEqual('money', close_synonyms[0][0])
        self.assertTrue(close_synonyms[0][1] >= close_similarity)
        self.assertEqual('cash', close_synonyms[1][0])
        self.assertTrue(close_synonyms[1][1] >= close_similarity)

        no_synonyms = sut.find_synonyms([10, 5, 0], 0.5)
        self.assertEqual(0, len(no_synonyms))

    def test_find_synonyms_by_word(self):
        sut = vt.NamedVectors(3)
        sut.add_vector('money', np.array([0, 0, 3]))
        sut.add_vector('cash', np.array([0.2, 0.3, 2.5]))
        sut.add_vector('currency', np.array([0.5, 0.7, 1.5]))
        sut.add_vector('sand', np.array([-0.5, 0.7, -1.5]))

        synonyms = sut.find_synonyms_by_word('cash', 0.9)

        self.assertEqual(2, len(synonyms))
        self.assertEqual('money', synonyms[0][0])
        self.assertEqual('currency', synonyms[1][0])

    def test_find_similar(self):
        sut = vt.NamedVectors(3)
        sut.add_vector('money', np.array([0, 0, 3]))
        sut.add_vector('cash', np.array([0.2, 0.3, 2.5]))
        sut.add_vector('currency', np.array([0.5, 0.7, 1.5]))
        sut.add_vector('void', np.array([-1, -1, -1]))
        sut.add_vector('bfgg', np.array([0, 0, 0]))

        sim1 = sut.find_similar([0, 0, 3], 1)
        self.assertEqual(1, len(sim1))
        self.assertEqual('money', sim1[0].name)

        sim2 = sut.find_similar([0, 0, 2.9], 3)
        self.assertEqual(3, len(sim2))
        self.assertEqual('money', sim2[0].name)
        self.assertEqual('cash', sim2[1].name)
        self.assertEqual('currency', sim2[2].name)

    def test_vector_from_expression(self):
        sut = vt.NamedVectors(3)
        sut.add_vector('king', np.array([1, 1, 0.1]))
        sut.add_vector('man', np.array([1, 0, 0.1]))
        sut.add_vector('queen', np.array([-1, 1, -0.1]))
        sut.add_vector('woman', np.array([-1, 0, -0.1]))

        result = sut.vector_from_expression(['king', '-', 'man', '+', 'woman'])
        npt.assert_array_equal(vt.normalize(np.array([-1, 1, -0.1])), result)


if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)
