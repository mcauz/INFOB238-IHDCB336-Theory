import re
from typing import Annotated
from fastapi import Cookie, HTTPException, status, Request, Header
from server.models import User
from server.repositories import AuthRepository


def create_auth_interceptor(SessionDep):
    class Auth:
        async def get_user(self, db_session: SessionDep, authorization: Annotated[str | None, Header()] = None) -> User | None:
            """
            Retrieves the user from the authentication token.

            Parameters
            ----------
            db_session : Session
                The session to access the database.
            authorization : Annotated[str | None, Header()], optional
                The authorization header used to retrieve the token, by default None.

            Returns
            -------
            User | None
                The user from the authentication token, or None if the token is invalid.
            """
            if authorization is None:
                return None

            matches = re.search("^Bearer (.+)$", authorization)
            if matches is None:
                return None

            token = matches.group(1)
            auth_repository = AuthRepository(db_session)
            return await auth_repository.decode_authentication_token(token)

        async def unauthorized_auth(
                self,
                request: Request,
                db_session: SessionDep,
                authorization: Annotated[str | None, Header()] = None
        ):
            """
            Throws an unauthorized exception if the user is not authenticated. Otherwise, add the user information
            in the request state.

            Parameters
            ----------
            request : Request
                The request information.
            db_session : Session
                The session to access the database.
            authorization : Annotated[str | None, Header()], optional
                The authorization header used to retrieve the token, by default None.
            """
            user = await self.get_user(db_session, authorization)

            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged.")

            request.state.user = user

    return Auth()
