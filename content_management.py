def Content():
    """
    This function returns a dictionary with all the content
    """
    PAGE_DICTIONARY = {"Track":[["Track intake","/Track_Intake/"],
                                 ["Add recipe","/Add_Recipe/"],
                                 ["Add ingredient","/Add_Ingredient/"],
                                 ["Private diary","/Private_Diary/"],
                                 ["Friends diary","/Friends_Diary/"]],
                        "Workout":[["Training today","/Training_Today/"],
                                 ["Line Graph","/Weight_Line/"]],
                        "Social":[["Friends","/Friends/"],
                                  ["Recipes","/Social_Recipes/"],
                                  ["Ingredients","/Social_Ingredients/"],
                                  ]}
    return PAGE_DICTIONARY