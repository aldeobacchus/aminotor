# Nouvelles caractéristiques
new_features = ['Barbe_de_3_jours', 'Sourcils_Arqués', None, 'Cernes', 'Chauve', 'Frange', 'Grosses_Levres', 'Gros_Nez', 'Cheveux_noirs', 'Cheveux_blonds', None, 
                'Cheveux_Bruns', 'Sourcils_Broussailleux', None, 'Double_Menton', 'Lunettes', 'Bouc', 'Cheveux_Gris', 'Maquillage', 'Pommettes_Hautes', 'Homme', 
                'Bouche_Entrouverte', 'Moustache', 'Yeux_Etroits', 'Pas_de_barbe', 'Visage_Oval', None, 'Nez_Pointu', 'Calvitie', None, 
                None, 'Sourire', 'Cheveux_Lisses', 'Cheveux_Ondules', 'Boucles_dOreilles', 'Chapeau', 'Rouge_A_Levres', 'Collier', 'Cravate', 
                'Age']

features = ['Barbe_de_3_jours', 'Sourcils_Arqués', 'Attirant', 'Cernes', 'Chauve', 'Frange', 'Grosses_Levres', 'Gros_Nez', 'Cheveux_noirs', 'Cheveux_blonds', 'Flou', 
                'Cheveux_Bruns', 'Sourcils_Broussailleux', 'Dodu', 'Double_Menton', 'Lunettes', 'Bouc', 'Cheveux_Gris', 'Maquillage', 'Pommettes_Hautes', 'Homme', 
                'Bouche_Entrouverte', 'Moustache', 'Yeux_Etroits', 'Pas_de_barbe', 'Visage_Oval', 'Peau_Pale', 'Nez_Pointu', 'Calvitie', 'Joues_Roses', 
                'Rouflaquettes', 'Sourire', 'Cheveux_Lisses', 'Cheveux_Ondules', 'Boucles_dOreilles', 'Chapeau', 'Rouge_A_Levres', 'Collier', 'Cravate', 
                'Age']

# Nouvelles questions pour les caractéristiques
new_questions = {
    'Barbe_de_3_jours': 'Le personnage a-t-il une barbe de trois jours?',
    'Sourcils_Arqués': 'Le personnage a-t-il des sourcils arqués?',
    'Attirant': 'Le personnage est-il considéré comme attirant?',
    'Cernes': 'Le personnage a-t-il des cernes sous les yeux?',
    'Chauve': 'Le personnage est-il chauve?',
    'Frange': 'Le personnage a-t-il une frange?',
    'Grosses_Levres': 'Le personnage a-t-il de grosses lèvres?',
    'Gros_Nez': 'Le personnage a-t-il un gros nez?',
    'Cheveux_noirs': 'Le personnage a-t-il des cheveux noirs?',
    'Cheveux_blonds': 'Le personnage a-t-il des cheveux blonds?',
    'Flou': "L'image est-elle floue?",
    'Cheveux_Bruns': 'Le personnage a-t-il des cheveux bruns?',
    'Sourcils_Broussailleux': 'Le personnage a-t-il des sourcils broussailleux?',
    'Dodu': 'Le personnage est-il dodu?',
    'Double_Menton': 'Le personnage a-t-il un double menton?',
    'Lunettes': 'Le personnage porte-t-il des lunettes?',
    'Bouc': 'Le personnage a-t-il un bouc?',
    'Cheveux_Gris': 'Le personnage a-t-il des cheveux gris?',
    'Maquillage': 'Le personnage porte-t-il du maquillage?',
    'Pommettes_Hautes': 'Le personnage a-t-il des pommettes hautes?',
    'Homme': 'Le personnage est-il un homme?',
    'Bouche_Entrouverte': 'La bouche du personnage est-elle légèrement ouverte?',
    'Moustache': 'Le personnage a-t-il une moustache?',
    'Yeux_Etroits': 'Le personnage a-t-il des yeux étroitements fermés?',
    'Pas_de_barbe': 'Le personnage est-il rasé de près (ou n\'a pas de barbe)?',
    'Visage_Oval': 'Le personnage a-t-il un visage ovale?',
    'Peau_Pale': 'Le personnage a-t-il la peau pâle?',
    'Nez_Pointu': 'Le personnage a-t-il un nez pointu?',
    'Calvitie': 'Le personnage a-t-il un début de calvitie?',
    'Joues_Roses': 'Le personnage a-t-il des joues roses?',
    'Rouflaquettes': 'Le personnage a-t-il des rouflaquettes?',
    'Sourire': 'Le personnage sourit-il?',
    'Cheveux_Lisses': 'Le personnage a-t-il des cheveux raides?',
    'Cheveux_Ondules': 'Le personnage a-t-il des cheveux ondulés?',
    'Boucles_dOreilles': "Le personnage porte-t-il des boucles d'oreilles?",
    'Chapeau': 'Le personnage porte-t-il un chapeau?',
    'Rouge_A_Levres': 'Le personnage porte-t-il du rouge à lèvres?',
    'Collier': 'Le personnage porte-t-il un collier?',
    'Cravate': 'Le personnage porte-t-il une cravate?',
    'Age': 'Le personnage est-il jeune?'
}

answers = {
    'Barbe_de_3_jours': ['Non, le personnage n\'a pas de barbe de trois jours.', 'Oui, le personnage a une barbe de trois jours.'],
    'Sourcils_Arqués': ['Non, le personnage n\'a pas des sourcils arqués.', 'Oui, le personnage a des sourcils arqués.'],
    'Attirant': ['Non, le personnage n\'est pas considéré comme attirant.', 'Oui, le personnage est considéré comme attirant.'],
    'Cernes': ['Non, le personnage n\'a pas de cernes sous les yeux.', 'Oui, le personnage a des cernes sous les yeux.'],
    'Chauve': ['Non, le personnage n\'est pas chauve.', 'Oui, le personnage est chauve.'],
    'Frange': ['Non, le personnage n\'a pas de frange.', 'Oui, le personnage a une frange.'],
    'Grosses_Levres': ['Non, le personnage n\'a pas de grosses lèvres.', 'Oui, le personnage a de grosses lèvres.'],
    'Gros_Nez': ['Non, le personnage n\'a pas un gros nez.', 'Oui, le personnage a un gros nez.'],
    'Cheveux_noirs': ['Non, le personnage n\'a pas des cheveux noirs.', 'Oui, le personnage a des cheveux noirs.'],
    'Cheveux_blonds': ['Non, le personnage n\'a pas des cheveux blonds.', 'Oui, le personnage a des cheveux blonds.'],
    'Flou': ['Non, l\'image n\'est pas floue.', 'Oui, l\'image est floue.'],
    'Cheveux_Bruns': ['Non, le personnage n\'a pas des cheveux bruns.', 'Oui, le personnage a des cheveux bruns.'],
    'Sourcils_Broussailleux': ['Non, le personnage n\'a pas des sourcils broussailleux.', 'Oui, le personnage a des sourcils broussailleux.'],
    'Dodu': ['Non, le personnage n\'est pas dodu.', 'Oui, le personnage est dodu.'],
    'Double_Menton': ['Non, le personnage n\'a pas de double menton.', 'Oui, le personnage a un double menton.'],
    'Lunettes': ['Non, le personnage ne porte pas de lunettes.', 'Oui, le personnage porte des lunettes.'],
    'Bouc': ['Non, le personnage n\'a pas de bouc.', 'Oui, le personnage a un bouc.'],
    'Cheveux_Gris': ['Non, le personnage n\'a pas des cheveux gris.', 'Oui, le personnage a des cheveux gris.'],
    'Maquillage': ['Non, le personnage ne porte pas de maquillage.', 'Oui, le personnage porte du maquillage.'],
    'Pommettes_Hautes': ['Non, le personnage n\'a pas des pommettes hautes.', 'Oui, le personnage a des pommettes hautes.'],
    'Homme': ['Non, le personnage n\'est pas masculin.', 'Oui, le personnage est masculin.'],
    'Bouche_Entrouverte': ['Non, la bouche du personnage n\'est pas légèrement ouverte.', 'Oui, la bouche du personnage est légèrement ouverte.'],
    'Moustache': ['Non, le personnage n\'a pas de moustache.', 'Oui, le personnage a une moustache.'],
    'Yeux_Etroits': ['Non, le personnage n\'a pas des yeux étroitement fermés.', 'Oui, le personnage a des yeux étroitement fermés.'],
    'Pas_de_barbe': ['Non, le personnage n\'est pas rasé de près.', 'Oui, le personnage est rasé de près.'],
    'Visage_Oval': ['Non, le personnage n\'a pas un visage ovale.', 'Oui, le personnage a un visage ovale.'],
    'Peau_Pale': ['Non, le personnage n\'a pas la peau pâle.', 'Oui, le personnage a la peau pâle.'],
    'Nez_Pointu': ['Non, le personnage n\'a pas un nez pointu.', 'Oui, le personnage a un nez pointu.'],
    'Calvitie': ['Non, le personnage n\'a pas un début de calvitie.', 'Oui, le personnage a un début de calvitie.'],
    'Joues_Roses': ['Non, le personnage n\'a pas des joues roses.', 'Oui, le personnage a des joues roses.'],
    'Rouflaquettes': ['Non, le personnage n\'a pas des rouflaquettes.', 'Oui, le personnage a des rouflaquettes.'],
    'Sourire': ['Non, le personnage ne sourit pas.', 'Oui, le personnage sourit.'],
    'Cheveux_Lisses': ['Non, le personnage n\'a pas des cheveux raides.', 'Oui, le personnage a des cheveux raides.'],
    'Cheveux_Ondules': ['Non, le personnage n\'a pas des cheveux ondulés.', 'Oui, le personnage a des cheveux ondulés.'],
    'Boucles_dOreilles': ['Non, le personnage ne porte pas de boucles d\'oreilles.', 'Oui, le personnage porte des boucles d\'oreilles.'],
    'Chapeau': ['Non, le personnage ne porte pas de chapeau.', 'Oui, le personnage porte un chapeau.'],
    'Rouge_A_Levres': ['Non, le personnage ne porte pas de rouge à lèvres', 'Oui, le personnage porte du rouge à lèvres.'],
    'Collier': ['Non, le personnage ne porte pas de collier.', 'Oui, le personnage porte un collier.'],
    'Cravate': ['Non, le personnage ne porte pas de cravate.', 'Oui, le personnage porte une cravate.'],
    'Age': ['Non, le personnage n\'est pas jeune.', 'Oui, le personnage est jeune.'],
    }


# Proba features
proba_features = [  0.9008, 0.7902, 0.7648, 0.805, 0.9752, 0.9252, 0.7598, 0.8002, 0.874, 
                    0.9284, 0.9532, 0.8348, 0.8916, 0.9464, 0.9542, 0.9752, 0.9508, 0.9698, 0.8886, 0.84, 
                    0.9406, 0.8578, 0.9622, 0.8882, 0.9098, 0.722, 0.9618, 0.7334, 0.9222, 0.9416, 0.9506, 
                    0.8876, 0.7758, 0.7714,0.8364, 0.975, 0.9052, 0.858, 0.946, 0.8372]

