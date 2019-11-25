"""
Name: Organization Hierarchy Tests
Author: Robert Ciborowski
Date: 13/11/2019
Description: CSC148 Assignment 2 - Tests for organization hierarchy classes
"""
import organization_hierarchy


def test_merge_empty() -> None:
    """Tests merge."""
    result = organization_hierarchy.merge([], [])
    assert len(result) == 0


def test_merge_first_is_empty() -> None:
    """Tests merge."""
    result = organization_hierarchy.merge([], [1, 2, 3])
    assert result == [1, 2, 3]


def test_merge_second_is_empty() -> None:
    """Tests merge."""
    result = organization_hierarchy.merge([1, 2, 3], [])
    assert result == [1, 2, 3]


def test_merge_single_items() -> None:
    """Tests merge."""
    result = organization_hierarchy.merge([1], [2])
    assert result == [1, 2]


def test_merge_same_items() -> None:
    """Tests merge."""
    result = organization_hierarchy.merge([1, 2, 3], [1, 2, 3])
    assert result == [1, 1, 2, 2, 3, 3]


def test_merge_many_items() -> None:
    """Tests merge."""
    result = organization_hierarchy.merge([135, 148, 157, 207, 209], [136, 137,
                                                                      165, 240])
    assert result == [135, 136, 137, 148, 157, 165, 207, 209, 240]


if __name__ == '__main__':
    import pytest

    pytest.main(['test_merge.py'])
