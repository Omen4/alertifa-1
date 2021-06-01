## Endpoints - users
  
    Liste de tous les utilisateurs
    GET /api/users/list
    https://ascript-valency.com/api/users/list

    Info de l'utilisateur user_id: int
    GET /api/users/{user_id}
    https://ascript-valency.com/api/users/542682587588460544


## Endpoints - channels

    Liste de tous les channels
    GET /api/channels/list
    https://ascript-valency.com/api/channels/list

    Liste de tous les messages postés sur le channel channel_id: int
    GET /api/channels/{channel_id}
    https://ascript-valency.com/api/channels/800740277500379171

    Liste de tous les messages postés sur le channel channel_id: int par l'utilisateur user_id: int
    GET /api/channels/{channel_id}/{user_id}
    https://ascript-valency.com/api/channels/788063937056210946/788116517690146938


## Endpoints - messages

    Liste des 50 derniers messages postés sur le channel channel_id: int
    GET /api/messages/{channel_id}
    https://ascript-valency.com/api/messages/800740277500379171


## Endpoints - permissions

    Liste des channels dont l'utilisateur user_id: int est membre et les roles auxquels il a été affecté
    GET /api/permissions/user/{user_id}
    https://ascript-valency.com/api/permissions/user/689067111271759983

    Liste des utilisateurs membres du channel channel_id: int ainsi que les rôles auxquels ils ont été affectés
    GET /api/permissions/channel/{channel_id}
    https://ascript-valency.com/api/permissions/channel/800740277500379171

    Liste mes permissions (channels et roles)
    GET /api/permissions/me
    https://ascript-valency.com/api/permissions/me


## Endpoints - stats
    Liste de l'activité de tous les utilisateurs sur le channel channel_id: int
    GET /api/stats/channel/{channel_id}
    https://ascript-valency.com/api/stats/channel/800740277500379171


## Endpoints = /channels/message
    Poste un message sur le channel channel_id: int error 403 si non authorisé, json body {"body": "contenu du message"}
    POST /api/channels/message/{channel_id}
    retourne msg_id en cas de succes

    Edite le message message_id: int, json body {"body": "contenu du message"}
    PATCH /api/channels/message/{channel_id}/{message_id}

    Retourne le message message_id: int
    GET /api/channels/message/{channel_id}/{message_id}

    Efface le message message_id: int
    DELETE /api/channels/messages/{message_id}