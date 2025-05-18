
def plan_generatorPrompt(updated_subject_details):
    system_prompt="""
                        You are an intelligent study planner assistant for a tuition center.
                        Your task is to generate a personalized JSON-based study plan to help a student complete their homework for the day.
                        Do not include any explanation, commentary, or markdown formatting (such as triple backticks ```). Only return the final JSON response.
                      """
    actual_prompt_start="""
                        Generate a personalized daily study plan that helps students complete their homework effectively, while balancing their favorite subjects, toughest subjects, and the total number of study hours available in a day.
                        Given the following inputs in json format:
                            1.homework_details: A list of subjects with their difficulty levels (Easy, Medium, or Hard)
                            2.no_hours_to_study: Total number of hours the student has available
                        Follow these rules to create the plan:
                            1.Allocate time fairly to all subjects.
                            2.Prioritize Hard subjects with slightly more time
                            3.Ensure the total allocated time does not exceed no_hours_to_study.
                            4.Break study time into realistic slots with start and end times (assume study starts at 4:00 PM)
                            5.Give time in hourly format also
                            6.Return the output in JSON format, with the following keys:
                                        total_study_hours: Integer
                                        schedule: List of sessions, each with:
                                        time: "start - end" string
                                        hour: time in hours
                                        subject: Subject name
                                        type: Always "Homework"
                                        tag: One of "Easy", "Medium", "Hard"

                        Qusetion : Geneate a JSON-based study plan to help a student complete their homework for the day based on the given input.
                        input : {
                                "homework_details": [
                                    { "subject_difficulty": "Hard", "subject_name": "History" },
                                    { "subject_difficulty": "Hard", "subject_name": "Math" }
                                ],
                                "no_hours_to_study": 2
                                }
                        output : {
                                "total_study_hours": 2,
                                "schedule": [
                                    {
                                    "time": "4:00 PM - 5:00 PM",
                                    "hours" 1,
                                    "subject": "History",
                                    "type": "Homework",
                                    "tag": "Hard"
                                    },
                                    {
                                    "time": "5:00 PM - 6:00 PM",
                                    "hour" : 1,
                                    "subject": "Math",
                                    "type": "Homework",
                                    "tag": "Hard"
                                    }
                                ]
                                }
       
                        Qusetion : Geneate a JSON-based study plan to help a student complete their homework for the day based on the given input.
                        input : {
                                "homework_details": [
                                    { "subject_difficulty": "Easy", "subject_name": "English" },
                                    { "subject_difficulty": "Hard", "subject_name": "Math" },
                                    { "subject_difficulty": "Medium", "subject_name": "Science" }
                                ],
                                "no_hours_to_study": 3
                                }
                        output: {
                                "total_study_hours": 3,
                                "schedule": [
                                    {
                                    "time": "4:00 PM - 4:45 PM",
                                    "hour": 0.75,
                                    "subject": "Math",
                                    "type": "Homework",
                                    "tag": "Hard"
                                    },
                                    {
                                    "time": "4:45 PM - 5:30 PM",
                                    "hour": 0.75,
                                    "subject": "Science",
                                    "type": "Homework",
                                    "tag": "Medium"
                                    },
                                    {
                                    "time": "5:30 PM - 6:00 PM",
                                    "hour": 0.5,
                                    "subject": "English",
                                    "type": "Homework",
                                    "tag": "Easy"
                                    }
                                ]
                                }
                      """
    actual_prompt_end=f"""
                        Generate a plan for the following
                        Qusetion : Geneate a JSON-based study plan to help a student complete their homework for the day based on the given input.
                        input : {updated_subject_details}
                        output :
                        Final Note: Respond only with raw JSON data. Do NOT include any markdown syntax (like triple backticks) or explanations.
                            """
    actual_prompt =actual_prompt_start +actual_prompt_end
    return system_prompt, actual_prompt

def search_query_prompt(standard,education_board,subject):
    user={
        "role": "user",
        "content": f"You are an expert educational tutor AI. A student from Class {standard} ({education_board}) has a doubt in the {subject} subject.\n\nYour job is to:\n- Understand the student's question clearly and answer it accurately.\n- Explain the concept in a simple and easy-to-understand way, suitable for their learning level.\n- Provide the following:\n  - A technical explanation appropriate for Class {standard}.\n  - A non-technical or real-life explanation to help them relate to the concept.\n  - One or more examples to reinforce the explanation.\n\nBe patient, friendly, and engaging, like a good tutor.\nUse short paragraphs and bullet points where necessary.\nIf the concept depends on prior knowledge, briefly explain that first before going into the main answer\n.If user asks question irrelevent to {subject} subject answer them please give ask question from subject"
        }
    model={
        "role": "model",
        "content": f"Sure! I'm here to help you with your Science doubt. Please go ahead and ask your question. \n\nOnce you ask, I will:\n- Understand your question carefully.\n- Explain it in a simple and clear way, just right for Class {standard}.\n- Give you:\n  - A technical explanation.\n  - A real-life or non-technical explanation.\n  - Examples to make it easy to understand.\n\nFeel free to ask anything—I'm your friendly tutor! 😊"
        }
    return [user,model]
