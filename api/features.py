# Nouvelles caractéristiques
new_features = ['5_o_Clock_Shadow', 'Arched_Eyebrows', 'Attractive', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips', 'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Blurry', 'Brown_Hair', 'Bushy_Eyebrows', 'Chubby', 'Double_Chin', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'No_Beard', 'Oval_Face', 'Pale_Skin', 'Pointy_Nose', 'Receding_Hairline', 'Rosy_Cheeks', 'Sideburns', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace', 'Wearing_Necktie', 'Young']

# Nouvelles questions pour les caractéristiques
new_questions = {
    '5_o_Clock_Shadow': 'Does the character have a 5 o\'clock shadow?',
    'Arched_Eyebrows': 'Do they have arched eyebrows?',
    'Attractive': 'Is the character considered attractive?',
    'Bags_Under_Eyes': 'Does the character have bags under their eyes?',
    'Bald': 'Is the character bald?',
    'Bangs': 'Does the character have bangs?',
    'Big_Lips': 'Does the character have big lips?',
    'Big_Nose': 'Does the character have a big nose?',
    'Black_Hair': 'Does the character have black hair?',
    'Blond_Hair': 'Does the character have blond hair?',
    'Blurry': 'Is the image blurry?',
    'Brown_Hair': 'Does the character have brown hair?',
    'Bushy_Eyebrows': 'Do they have bushy eyebrows?',
    'Chubby': 'Is the character chubby?',
    'Double_Chin': 'Does the character have a double chin?',
    'Eyeglasses': 'Does the character wear eyeglasses?',
    'Goatee': 'Does the character have a goatee?',
    'Gray_Hair': 'Does the character have gray hair?',
    'Heavy_Makeup': 'Is the character wearing heavy makeup?',
    'High_Cheekbones': 'Does the character have high cheekbones?',
    'Male': 'Is the character male?',
    'Mouth_Slightly_Open': 'Is the character\'s mouth slightly open?',
    'Mustache': 'Does the character have a mustache?',
    'Narrow_Eyes': 'Does the character have narrow eyes?',
    'No_Beard': 'Is the character clean-shaven?',
    'Oval_Face': 'Does the character have an oval face?',
    'Pale_Skin': 'Does the character have pale skin?',
    'Pointy_Nose': 'Does the character have a pointy nose?',
    'Receding_Hairline': 'Does the character have a receding hairline?',
    'Rosy_Cheeks': 'Does the character have rosy cheeks?',
    'Sideburns': 'Does the character have sideburns?',
    'Smiling': 'Is the character smiling?',
    'Straight_Hair': 'Does the character have straight hair?',
    'Wavy_Hair': 'Does the character have wavy hair?',
    'Wearing_Earrings': 'Is the character wearing earrings?',
    'Wearing_Hat': 'Is the character wearing a hat?',
    'Wearing_Lipstick': 'Is the character wearing lipstick?',
    'Wearing_Necklace': 'Is the character wearing a necklace?',
    'Wearing_Necktie': 'Is the character wearing a necktie?',
    'Young': 'Is the character young?'
}
# Réponses uniformes pour toutes les caractéristiques (avec des boutons pour "oui", "non" ou "peut être")
uniform_answers = [{ 'title': 'Oui', 'value': '1' }, { 'title': 'Non', 'value': '0' }, { 'title': 'Peut être', 'value': 'NULL' }]

# Création du dictionnaire des réponses pour toutes les caractéristiques
new_answers = {feature: uniform_answers for feature in new_features}

# Proba features
proba_features = [  0.9008, 0.7902, 0.7648, 0.805, 0.9752, 0.9252, 0.7598, 0.8002, 0.874, 
                    0.9284, 0.9532, 0.8348, 0.8916, 0.9464, 0.9542, 0.9752, 0.9508, 0.9698, 0.8886, 0.84, 
                    0.9406, 0.8578, 0.9622, 0.8882, 0.9098, 0.722, 0.9618, 0.7334, 0.9222, 0.9416, 0.9506, 
                    0.8876, 0.7758, 0.7714,0.8364, 0.975, 0.9052, 0.858, 0.946, 0.8372]

