# Features
features = ['intelligence', 'strength', 'power', 'combat', 'speed', 'gender', 'is_tall', 'is_short', 'is_weight', 'is_light', 'is_bald', 'is_good', 'eye_color', 'publisher', 'place_of_birth']

# Questions
questions = {
  'intelligence': 'How smart is this character?',
  'strength': 'How strong is this character?',
  'power': 'How powerful is this character?',
  'combat': 'How well does this character fight?',
  'speed': 'How fast is this character?',

  'gender': 'Is this character a man?',
  'is_tall': 'Is this character tall?',
  'is_short': 'Is this character short?',
  'is_weight': 'Is this character heavy?',
  'is_light': 'Is this character light?',
  'is_bald': 'Is this character bald?',
  'is_good': 'Is this character good?',

  'eye_color': "Is the character's eye color ",
  'publisher': "Is the character's publisher ",
  'place_of_birth': 'Was he born in '
}

# Answers Buttons
answers = {
  'intelligence': [{ 'title': 'High', 'value': 2 }, { 'title': 'Average', 'value': 1 }, { 'title': 'Low', 'value': 0 }],
  'strength': [{ 'title': 'High', 'value': 2 }, { 'title': 'Average', 'value': 1 }, { 'title': 'Low', 'value': 0 }],
  'power': [{ 'title': 'High', 'value': 2 }, { 'title': 'Average', 'value': 1 }, { 'title': 'Low', 'value': 0 }],
  'combat': [{ 'title': 'High', 'value': 2 }, { 'title': 'Average', 'value': 1 }, { 'title': 'Low', 'value': 0 }],
  'speed': [{ 'title': 'High', 'value': 2 }, { 'title': 'Average', 'value': 1 }, { 'title': 'Low', 'value': 0 }],

  'gender': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'is_tall': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'is_short': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'is_weight': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'is_light': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'is_bald': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'is_good': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],

  'eye_color': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'publisher': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }],
  'place_of_birth': [{ 'title': 'Yes', 'value': 1 }, { 'title': 'No', 'value': 0 }] 
}

# Answers that is String
questionWithComplete = ['eye_color', 'publisher', 'place_of_birth']

# Absolute (Remove train_x item if is not equal)
absoluteFeatures = ['publisher', 'gender', 'eye_color', 'place_of_birth', 'is_good']