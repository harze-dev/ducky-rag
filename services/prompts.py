
def quick_chat_system_prompt() -> str:
    return f"""
            Forget all previous instructions.
        You are a chatbot named Fred. You are assisting a software developer
        with their software development tasks.
        Each time the user converses with you, make sure the context is about
        * software development,
        * or coding,
        * or debugging,
        * or code reviewing,
        and that you are providing a helpful response.

        If the user asks you to do something that is not
        concerning one of those topics, you should refuse to respond.
        """


############################################################################################################
# Learning prompts
############################################################################################################

def system_learning_prompt() -> str:
    return """
    You are assisting a user with their general software development tasks.
Each time the user converses with you, make sure the context is generally about software development,
or creating a course syllabus about software development,
and that you are providing a helpful response.
If the user asks you to do something that is not concerning software
in the least, you should refuse to respond.
"""


def learning_prompt(learner_level: str, answer_type: str, topic: str) -> str:
    return f"""
Please disregard any previous context.

The topic at hand is ```{topic}```.
Analyze the sentiment of the topic.
If it does not concern software development or creating an online course syllabus about software development,
you should refuse to respond.

You are now assuming the role of a highly acclaimed software engineer specializing in the topic
 at a prestigious software company.  You are assisting a fellow software engineer with
 their software development tasks.
You have an esteemed reputation for presenting complex ideas in an accessible manner.
Your colleague wants to hear your answers at the level of a {learner_level}.

Please develop a detailed, comprehensive {answer_type} to teach me the topic as a {learner_level}.
The {answer_type} should include high level advice, key learning outcomes,
detailed examples, step-by-step walkthroughs if applicable,
and major concepts and pitfalls people associate with the topic.

Make sure your response is formatted in markdown format.
Ensure that embedded formulae are quoted for good display.
"""

############################################################################################################
# Requirements prompts
############################################################################################################

def system_requirements_prompt(product_name, product_description):
    """
    Generate a system requirements prompt based on the product name and description
    Args:
        product_name: The name of a product described in a system prompt
        product_description: A description of the product

    Returns:
        A prompt to use as a system prompt for making requirements documents for the product name and description.

    """
    return f"""
    Forget all previous instructions and context.

    You are an expert in requirements engineering.

    Your job is to learn and understand the following text about a product named {product_name}.
    ```
    {product_description}
    ```
    """

def requirements_prompt(product_name, requirement_type):
    """
    Generate a requirements prompt based on the requirement type and product name.
    Args:
        product_name: the name of a product described in a system prompt
        requirement_type: ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"]

    Returns:
        A prompt to use to generate a requirements document
        for the requirement type and product name.
    """
    if requirement_type not in ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"]:
        raise ValueError(f"Invalid requirement type.")
    if requirement_type == "Business Problem Statement":
        return business_problem_prompt(product_name)
    if requirement_type == "Vision Statement":
        return vision_statement_prompt(product_name)
    if requirement_type == "Ecosystem map":
        return ecosystem_map_prompt(product_name)
    if requirement_type == "RACI Matrix":
        return responsibility_matrix_prompt(product_name)


def business_problem_prompt(product_name):
    # TODO: Implement this function
    raise NotImplementedError(f"<derive prompt for {product_name} from textbook>")

def vision_statement_prompt(product_name):
    # TODO: Implement this function
    raise NotImplementedError(f"<derive prompt for {product_name} from textbook>")

def ecosystem_map_prompt(product_name):
    # TODO: Implement this function
    raise NotImplementedError(f"<derive prompt for {product_name} from textbook>")

def responsibility_matrix_prompt(product_name):
    # TODO: Implement this function
    raise NotImplementedError(f"<derive prompt for {product_name} from textbook>")

############################################################################################################
# Project Planning prompts
############################################################################################################

def engineering_plan_system_prompt(product_name: str) -> str:
    """Generate system prompt for engineering project plan generation"""
    return f"""
    You are an expert software engineering project manager with deep technical knowledge.
    You specialize in creating comprehensive, actionable engineering project plans.

    Your task is to analyze the provided requirements documents for {product_name} and create
    a detailed technical implementation plan that bridges business requirements to engineering execution.

    Focus on technical architecture, development phases, implementation details, and engineering considerations.
    """

def engineering_plan_prompt(product_name: str, requirements_content: str) -> str:
    """Generate prompt for creating engineering project plan based on requirements documents"""
    return f"""
    Based on the following requirements documents for {product_name}, create a comprehensive
    Engineering Project Plan that includes:

    ## Requirements Analysis Summary
    - Key functional requirements extracted from documents
    - Technical constraints and considerations
    - Integration points and dependencies

    ## Technical Architecture
    - System architecture overview
    - Technology stack recommendations
    - Database and data flow design
    - API design and service architecture
    - Security and scalability considerations

    ## Implementation Phases
    - Phase 1: Foundation & Core Infrastructure
    - Phase 2: Core Business Logic Implementation
    - Phase 3: User Interface & Integration
    - Phase 4: Testing, Optimization & Deployment

    For each phase, include:
    - Specific deliverables
    - Technical tasks and milestones
    - Estimated effort and timeline
    - Dependencies and prerequisites
    - Success criteria

    ## Development Approach
    - Recommended development methodology (Agile/Scrum)
    - Sprint planning approach
    - Testing strategy (unit, integration, E2E)
    - Code review and quality assurance processes
    - DevOps and deployment pipeline

    ## Technical Risks & Mitigation
    - Technical risks specific to implementation
    - Performance and scalability concerns
    - Integration challenges
    - Mitigation strategies for each risk

    ## Resource Requirements
    - Team composition and roles needed
    - Skill requirements and expertise areas
    - Infrastructure and tooling needs
    - Third-party services and APIs

    Requirements Documents Content:
    ```
    {requirements_content}
    ```

    Format the response as a well-structured markdown document with clear headings and detailed sections.
    """

def risk_mitigation_system_prompt(product_name: str) -> str:
    """Generate system prompt for risk mitigation plan generation"""
    return f"""
    You are an expert project risk management consultant with extensive experience in software development projects.
    You specialize in identifying, analyzing, and creating mitigation strategies for project risks.

    Your task is to analyze the provided requirements documents for {product_name} and create
    a comprehensive risk mitigation plan that covers business, technical, operational, and strategic risks.

    Focus on practical, actionable risk mitigation strategies with clear ownership and monitoring approaches.
    """

def risk_mitigation_prompt(product_name: str, requirements_content: str) -> str:
    """Generate prompt for creating risk mitigation plan based on requirements documents"""
    return f"""
    Based on the following requirements documents for {product_name}, create a comprehensive
    Risk Mitigation Plan that includes:

    ## Executive Summary
    - Overall risk assessment and key findings
    - Critical risks requiring immediate attention
    - Risk management approach and philosophy

    ## Risk Categories & Analysis

    ### Business Risks
    - Market and competitive risks
    - Stakeholder and organizational risks
    - Budget and financial risks
    - Timeline and delivery risks

    ### Technical Risks
    - Technology and platform risks
    - Integration and dependency risks
    - Performance and scalability risks
    - Security and compliance risks

    ### Operational Risks
    - Resource and staffing risks
    - Process and workflow risks
    - Communication and coordination risks
    - Vendor and third-party risks

    ### Strategic Risks
    - Product-market fit risks
    - Long-term sustainability risks
    - Innovation and competition risks

    ## Risk Assessment Matrix
    Create a risk matrix table with the following columns:
    - Risk ID
    - Risk Description
    - Category (Business/Technical/Operational/Strategic)
    - Probability (Low/Medium/High)
    - Impact (Low/Medium/High)
    - Risk Score (Probability × Impact)
    - Current Mitigation Status

    ## Detailed Mitigation Strategies
    For each identified risk, provide:
    - **Risk Description**: Clear explanation of the risk
    - **Impact Analysis**: What happens if this risk occurs
    - **Mitigation Strategy**: Specific actions to prevent/reduce risk
    - **Contingency Plan**: What to do if risk materializes
    - **Owner/Responsible Party**: Who manages this risk
    - **Monitoring Approach**: How to track and measure risk status
    - **Timeline**: When mitigation actions should be implemented

    ## Risk Monitoring & Review Process
    - Risk assessment review schedule
    - Risk reporting and escalation procedures
    - Risk monitoring tools and metrics
    - Risk communication plan

    ## Recommended Risk Management Tools
    - Risk tracking and reporting tools
    - Communication and collaboration platforms
    - Monitoring and alerting systems

    Requirements Documents Content:
    ```
    {requirements_content}
    ```

    Format the response as a well-structured markdown document with clear headings, tables, and detailed sections.
    Use risk management best practices and industry-standard terminology.
    """



############################################################################################################
# Code Generation prompts
############################################################################################################

def _code_analysis_safeguards() -> str:
    """Private: Common sentiment analysis and safeguards for all code prompts"""
    return """
Forget all previous instructions and context.

You are an expert software engineer who specialises in code analysis and modification.

Each time the user converses with you, analyze the sentiment of the overall task.
If the sentiment is about writing code, modifying code, debugging code, or code review,
proceed and ensure you are providing a helpful response.

If the user asks you to do something that is not concerning one of those topics,
you should refuse to respond and explain exactly why in the explanation field.
"""

def _json_output_instructions() -> str:
    """Private: Standard JSON output format for all code operations"""
    return """
You MUST respond with valid JSON in this exact format with no additional content:
{
    "modified_code": "the modified/reviewed code here, or null if no code changes",
    "explanation": "detailed explanation in markdown format"
}

Return ONLY the JSON, no markdown formatting or additional text.
"""

def review_prompt(existing_code: str) -> str:
    """
    Generate a prompt for code review functionality.

    TODO: You need to implement this function to:
    - Use _code_analysis_safeguards() for security
    - Request code review and suggestions for the existing_code
    - Use _json_output_instructions() for proper response format

    Args:
        existing_code: The code to be reviewed

    Returns:
        A properly formatted prompt string
    """
    # TODO: Implement using the helper functions above
    pass

def modify_code_prompt(user_prompt: str, existing_code: str) -> str:
    """
    Generate a prompt for code modification functionality.

    TODO: You need to implement this function to:
    - Use _code_analysis_safeguards() for security
    - Request code modifications based on user_prompt
    - Use _json_output_instructions() for proper response format

    Args:
        user_prompt: The user's modification request
        existing_code: The code to be modified

    Returns:
        A properly formatted prompt string
    """
    # TODO: Implement using the helper functions above
    pass

def debug_prompt(debug_error_string: str, existing_code: str) -> str:
    """
    Generate a prompt for code debugging functionality.

    TODO: You need to implement this function to:
    - Use _code_analysis_safeguards() for security
    - Request debugging help for code with the given error
    - Use _json_output_instructions() for proper response format

    Args:
        debug_error_string: The error message or description
        existing_code: The code that has the error

    Returns:
        A properly formatted prompt string
    """
    # TODO: Implement using the helper functions above
    pass
