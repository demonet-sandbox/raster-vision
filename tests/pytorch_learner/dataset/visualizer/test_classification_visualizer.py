from typing import Callable
import unittest

import torch

from rastervision.pytorch_learner.dataset import ClassificationVisualizer


class TestClassificationVisualizer(unittest.TestCase):
    def assertNoError(self, fn: Callable, msg: str = ''):
        try:
            fn()
        except Exception:
            self.fail(msg)

    def test_plot_batch(self):
        # w/o z
        viz = ClassificationVisualizer(
            class_names=['bg', 'fg'],
            channel_display_groups=dict(RGB=[0, 1, 2], IR=[3]))
        x = torch.randn(size=(2, 4, 256, 256))
        y = torch.tensor([0, 1])
        self.assertNoError(lambda: viz.plot_batch(x, y))

        # w/ z
        viz = ClassificationVisualizer(
            class_names=['bg', 'fg'],
            channel_display_groups=dict(RGB=[0, 1, 2], IR=[3]))
        x = torch.randn(size=(2, 4, 256, 256))
        y = torch.tensor([0, 1])
        z = torch.tensor([[0.9, 0.1], [0.6, 0.4]])
        self.assertNoError(lambda: viz.plot_batch(x, y, z=z))

        # w/ z, w/o y
        viz = ClassificationVisualizer(
            class_names=['bg', 'fg'],
            channel_display_groups=dict(RGB=[0, 1, 2], IR=[3]))
        x = torch.randn(size=(2, 4, 256, 256))
        y = None
        z = torch.tensor([[0.9, 0.1], [0.6, 0.4]])
        self.assertNoError(lambda: viz.plot_batch(x, y, z=z))

    def test_plot_batch_temporal(self):
        # w/o z
        viz = ClassificationVisualizer(
            class_names=['bg', 'fg'],
            channel_display_groups=dict(RGB=[0, 1, 2], IR=[3]))
        x = torch.randn(size=(2, 3, 4, 256, 256))
        y = torch.tensor([0, 1])
        self.assertNoError(lambda: viz.plot_batch(x, y))

        # w/ z
        viz = ClassificationVisualizer(
            class_names=['bg', 'fg'],
            channel_display_groups=dict(RGB=[0, 1, 2], IR=[3]))
        x = torch.randn(size=(2, 3, 4, 256, 256))
        y = torch.tensor([0, 1])
        z = torch.tensor([[0.9, 0.1], [0.6, 0.4]])
        self.assertNoError(lambda: viz.plot_batch(x, y, z=z))

        # w/ z, w/o y
        viz = ClassificationVisualizer(
            class_names=['bg', 'fg'],
            channel_display_groups=dict(RGB=[0, 1, 2], IR=[3]))
        x = torch.randn(size=(2, 3, 4, 256, 256))
        y = None
        z = torch.tensor([[0.9, 0.1], [0.6, 0.4]])
        self.assertNoError(lambda: viz.plot_batch(x, y, z=z))
