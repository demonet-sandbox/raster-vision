import os
import unittest

from sagemaker.workflow.pipeline import Pipeline as SageMakerPipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep

from rastervision.pipeline import rv_config_ as rv_config
from rastervision.aws_sagemaker.aws_sagemaker_runner import AWSSageMakerRunner


class MockPipeline:
    commands = ['analyze', 'chip', 'train', 'predict', 'eval']
    split_commands = ['chip', 'predict']
    gpu_commands = ['train', 'predict']


class TestAWSSageMakerRunner(unittest.TestCase):
    def setUp(self):
        rv_config.set_everett_config(
            config_overrides=dict(
                SAGEMAKER_role='AmazonSageMakerExecutionRole',
                SAGEMAKER_cpu_image='123.dkr.ecr.us-east-1.amazonaws.com/rv',
                SAGEMAKER_cpu_instance_type='ml.p3.2xlarge',
                SAGEMAKER_gpu_image='123.dkr.ecr.us-east-1.amazonaws.com/rv',
                SAGEMAKER_gpu_instance_type='ml.p3.2xlarge',
                SAGEMAKER_use_spot_instances='yes',
            ))
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    def test_build_pipeline(self):
        pipeline = MockPipeline()
        runner = AWSSageMakerRunner()
        rv_config.set_verbosity(4)
        sagemaker_pipeline = runner.build_pipeline(
            'config.json',
            pipeline,
            ['chip', 'train', 'predict', 'eval'],
            num_splits=2,
            pipeline_run_name='test',
        )
        self.assertIsInstance(sagemaker_pipeline, SageMakerPipeline)
        self.assertEqual(len(sagemaker_pipeline.steps), 6)
        # chip #1
        self.assertIsInstance(sagemaker_pipeline.steps[0], ProcessingStep)
        # chip #2
        self.assertIsInstance(sagemaker_pipeline.steps[1], ProcessingStep)
        # train
        self.assertIsInstance(sagemaker_pipeline.steps[2], TrainingStep)
        self.assertEqual(len(sagemaker_pipeline.steps[2].depends_on), 2)
        # predict #1
        self.assertIsInstance(sagemaker_pipeline.steps[3], TrainingStep)
        self.assertEqual(len(sagemaker_pipeline.steps[3].depends_on), 3)
        # predict #2
        self.assertIsInstance(sagemaker_pipeline.steps[4], TrainingStep)
        self.assertEqual(len(sagemaker_pipeline.steps[4].depends_on), 3)
        # eval
        self.assertIsInstance(sagemaker_pipeline.steps[5], ProcessingStep)
        self.assertEqual(len(sagemaker_pipeline.steps[5].depends_on), 5)


if __name__ == '__main__':
    unittest.main()
