#Propostion d'échéancier

## Sprint 1

Pour ce sprint, je propose que toutes les saisies soient faitent manuellement. Pas de média sociaux. On construit la base de l'applicaiton.

* Site web:
  * validation utilisateur (nom et mot de passe)
  * saisie des bénéficaires
  * saisie des intérêts
  * intégration avec site pour suggestion basée sur les intérêts des bénéficiaires
  * affichage des suggestion pour les différents bénéficaires

* Base de données:
  * user (userID, user_name, pernom, nom, password)
  * beneficiaires (clientID, prenom, nom, date_naissance)
  * interets (clientID, interets)
  * user_client (userID, clientID)

* Intégration avec sites:
  * Amazon
  * eBay

* Application mobile
  * N/A

## Sprint 2

Pour le sprint 2, nous allons de l'avant avec l'aggrégateur pour Facebook en plus de termner ce qui n'a pas été finalisé dans le sprint 1

* Correction d'erreurs

* Site web:
  * Permette la saisie des informations sur le compte Facebook
  * Permettre la suppression des entrées importées des médias sociaux

* Base de données:
  * user_social (userID, social_network, login, password)
  * beneficiaires (ajout champs pour dire si l'information est saisie ou importée)
  * interets (ajout pour dire si l'information a été importée ou saisie par l'utilisateur)

* Intégration avec sites:
  * Facebook

## Sprint 3

Pour le dernier sprint, en plus de la correction des annomalies, nous pourrions regarder le développement d'une première application mobile (si nous avons le temps)

* Site web:
  * N/A

* Base de données:
  * N/A

* Intégration avec sites:
  * N/A

* Application mobile:
  * Interface utilisateur