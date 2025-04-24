import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

class CICDPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub("santiagoarielv98/infrastructure", "main"),
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        )
                    )

    # def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    #     super().__init__(scope, construct_id, **kwargs)
        
    #     # Definir el pipeline
    #     pipeline = codepipeline.Pipeline(
    #         self, "LambdaAppPipeline",
    #         pipeline_name="lambda-app-pipeline",
    #         restart_execution_on_update=True
    #     )
        
    #     # Fuente desde GitHub
    #     source_output = codepipeline.Artifact()
    #     github_token = SecretValue.secrets_manager("github-token")
        
    #     source_action = codepipeline_actions.GitHubSourceAction(
    #         action_name="GitHub_Source",
    #         owner="your-github-username",
    #         repo="your-repo-name",
    #         branch="main",
    #         oauth_token=github_token,
    #         output=source_output
    #     )
        
    #     # Agregar etapa de fuente
    #     pipeline.add_stage(
    #         stage_name="Source",
    #         actions=[source_action]
    #     )
        
    #     # Definir un proyecto de CodeBuild para dev
    #     dev_project = codebuild.PipelineProject(
    #         self, "DevBuild",
    #         environment=codebuild.BuildEnvironment(
    #             build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
    #             privileged=True,
    #         ),
    #         environment_variables={
    #             "ENVIRONMENT": codebuild.BuildEnvironmentVariable(value="dev")
    #         },
    #         build_spec=codebuild.BuildSpec.from_source_filename('cicd/buildspec.yml')
    #     )
        
    #     # Agregar permisos para CDK
    #     dev_project.role.add_managed_policy(
    #         iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
    #     )
        
    #     # Agregar etapa de despliegue a dev
    #     dev_build_output = codepipeline.Artifact()
    #     dev_build_action = codepipeline_actions.CodeBuildAction(
    #         action_name="DeployToDev",
    #         project=dev_project,
    #         input=source_output,
    #         outputs=[dev_build_output]
    #     )
        
    #     pipeline.add_stage(
    #         stage_name="DeployToDev",
    #         actions=[dev_build_action]
    #     )
        
    #     # Definir un proyecto de CodeBuild para main (producción)
    #     main_project = codebuild.PipelineProject(
    #         self, "MainBuild",
    #         environment=codebuild.BuildEnvironment(
    #             build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
    #             privileged=True,
    #         ),
    #         environment_variables={
    #             "ENVIRONMENT": codebuild.BuildEnvironmentVariable(value="main")
    #         },
    #         build_spec=codebuild.BuildSpec.from_source_filename('cicd/buildspec.yml')
    #     )
        
    #     # Agregar permisos para CDK
    #     main_project.role.add_managed_policy(
    #         iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
    #     )
        
    #     # Agregar etapa de aprobación manual antes de despliegue a producción
    #     manual_approval_action = codepipeline_actions.ManualApprovalAction(
    #         action_name="ApproveDeployment",
    #         run_order=1
    #     )
        
    #     # Agregar etapa de despliegue a producción
    #     main_build_output = codepipeline.Artifact()
    #     main_build_action = codepipeline_actions.CodeBuildAction(
    #         action_name="DeployToMain",
    #         project=main_project,
    #         input=source_output,
    #         outputs=[main_build_output],
    #         run_order=2
    #     )
        
    #     pipeline.add_stage(
    #         stage_name="DeployToMain",
    #         actions=[manual_approval_action, main_build_action]
    #     )