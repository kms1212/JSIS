Authentification API Documentation
----------------------------------

Routes
======
.. dropdown:: /auth/login
    
    API Class Documentation: :class:`authapi.views.LoginAPI`

    .. tab-set::

        .. tab-item:: POST

            **Description**
            Login with username and password and get a authentication token.

            **Request**

            .. list-table::
                :widths: 30 70
                :header-rows: 1

                * - Key
                  - Value Description
                * - username
                  - Username
                * - password
                  - Password

            **Response**

            .. tab-set::
                .. tab-item:: HTTP 200

                    Login successful
                    After login, to access the protected routes, the auth token must be provided in the header.

                    :Authorization: `Token <token>`

                    **Return Values**

                    .. list-table::
                        :widths: 30 70
                        :header-rows: 1

                        * - Key
                          - Value Description
                        * - user
                          - :class:`authapi.models.UserAccount` object serialized by :class:`authapi.serializers.UserAccountSerializer`
                        * - token
                          - Authentication token

                .. tab-item:: HTTP 400

                    Bad request

                    **Return Values**
                    
                    .. list-table::
                        :widths: 30 70
                        :header-rows: 1

                        * - Key
                          - Value Description
                        * - message
                          - Error message

.. dropdown:: /auth/logout

    API Class Documentation:  `knox.views.LogoutView <https://james1345.github.io/django-rest-knox/views/#loginview>`_

    .. tab-set::

        .. tab-item:: POST

            **Description**
            Logout and invalidate the authentication token.

            **Request**

            None, but the auth token must be provided in the header.

            :Authorization: `Token <token>`

            **Response**

            .. tab-set::
                .. tab-item:: HTTP 204

                    Logout successful

                    **Return Values**

                    No return values

.. dropdown:: /auth/register

    API Class Documentation: :class:`authapi.views.RegisterAPI`

    .. tab-set::

        .. tab-item:: POST

            **Description**
            Register a new user.

            **Request**

            .. list-table::
                :widths: 30 70
                :header-rows: 1

                * - Key
                  - Value Description
                * - username
                  - Username
                * - visiblename
                  - Visible name(Nickname)
                * - password
                  - Password
                * - password_chk
                  - Password check (Removed in the future)
                * - email
                  - Email
                * - profileimage
                  - Profile image file (Optional)

            **Response**

            .. tab-set::
                .. tab-item:: HTTP 200

                    Register successful

                    **Return Values**

                    Detailed information of the registered user. See :class:`authapi.serializers.DetailedUserSerializer`

                    .. list-table::
                        :widths: 30 70
                        :header-rows: 1

                        * - Key
                          - Value Description
                        * - userid
                          - User id
                        * - username
                          - Username
                        * - visiblename
                          - Visible name(Nickname)
                        * - email
                          - Email
                        * - permission
                          - Permission level
                        * - studentid
                          - Student id
                        * - profileimage
                          - :class:`File` id of the profile image
                        * - Ddescription
                          - Description
                        * - date_joined
                          - Date joined
                        * - date_lastlogin
                          - Last login date
                        * - is_blocked
                          - Is blocked
                        * - is_blocked_anon
                          - Is blocked for anonymous service
                        * - block_reason
                          - Block reason
                        * - agreement_status
                          - Agreement status
                        * - post_count
                          - Count of :ref:`communityapi.models.Post`
                        * - reply_count
                          - Count of :ref:`bbsbaseapi.models.Reply`

                .. tab-item:: HTTP 400
                        
                    Bad request

                    **Return Values**
                    
                    .. list-table::
                        :widths: 30 70
                        :header-rows: 1

                        * - Key
                          - Value Description
                        * - message
                          - Error message

    