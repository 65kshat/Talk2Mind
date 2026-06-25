import random

ASSESSMENT_SCRIPTS = [

"""
Today has been a normal day.

I spent time thinking about my responsibilities.

Some moments were enjoyable and some were challenging.

I am taking a few minutes to complete this assessment.

I will continue working toward my goals.
""",

"""
I am describing my day in a calm and natural manner.

Everyone experiences different emotions throughout the week.

Some situations are easy while others require more effort.

I am focusing on reading these sentences clearly.

Thank you for listening.
""",

"""
Life contains both positive and negative experiences.

People react differently to the events around them.

Some days feel productive and energetic.

Other days feel slower and more demanding.

I am now finishing this short reading exercise.
""",

"""
I have experienced many different situations throughout my life.

Some memories make me smile while others make me think deeply.

Every day brings new opportunities and new challenges.

I try to learn from my experiences.

This assessment helps me reflect on my wellbeing.
""",

"""
Today I am taking part in a short wellbeing assessment.

I am reading these sentences in a natural voice.

My emotions may change from day to day.

My thoughts and feelings are important.

I am now reaching the end of this exercise.
"""
]


def get_random_script():
    return random.choice(ASSESSMENT_SCRIPTS)