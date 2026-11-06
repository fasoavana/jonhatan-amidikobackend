gestion admin fonctionnel avec ancien jwt
#########################################################
Fonctionnalité	Résultat
#########################################################

Lister les utilisateurs						Validé
Consulter un utilisateur					Validé
Suspendre un compte						Validé
Réactiver un compte						Validé
Supprimer logiquement un compte					Validé
Bloquer la connexion d'un compte suspendu			Validé
Bloquer la connexion d'un compte supprimé			Validé
########################################################
gestion admin fonctionnel avec nouveau jwt
########################################################
Connexion de l'utilisateur actif	200 OK			Validé
Accès à /me/ avec son token	200 OK				Validé
Suspension par l'administrateur	200 OK				Validé
Réutilisation de l'ancien token	401 Unauthorized		Validé
Utilisateur actif avec JWT	200 OK				Validé
Utilisateur suspendu avec ancien JWT	401			Validé
Utilisateur supprimé avec ancien JWT	401			Validé
Connexion d'un compte suspendu	Refusée				Validé
Connexion d'un compte supprimé	Refusée				Validé

L'inscription et la connexion des utilisateurs.			Validé
La gestion des rôles et des statuts.				Validé
La consultation des utilisateurs par l'administrateur.		Validé
La suspension et la suppression logique des comptes.		Validé
La protection des routes avec les access tokens JWT.		Validé
La protection du renouvellement des refresh tokens.		Validé

Consulter son profil						Validé
Consulter la liste des utilisateurs				Validé
Modifier le statut d'un utilisateur				Validé


Admin modifie le rôle d'un autre utilisateur	200 OK		Validé
Moderator tente de modifier un rôle	403 Forbidden		Validé
Admin tente de modifier son propre rôle	400 Bad Request		Validé



Consulter la liste des utilisateurs	200 OK			Validé
Modifier le statut d'un utilisateur	403 Forbidden		Validé
Modifier le rôle d'un utilisateur	403 Forbidden		Validé



Consulter son profil (GET)	200 OK				Validé
Modifier son profil (PATCH)	200 OK				Validé
Modifier son rôle via /me/	400 — Bloqué			Validé
Modifier son statut via /me/	Protection prévue par le serializer	Validé


Consulter son profil						Validé
Modifier son prénom						Validé
Modifier son nom						Validé
Modifier son téléphone						Validé
Modifier son rôle	Bloqué 					Validé
Modifier son statut	Bloqué 					Validé