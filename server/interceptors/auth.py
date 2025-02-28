from typing import Annotated
from fastapi import Cookie, HTTPException, status, Request
from server.models import User
from server.repositories import AuthRepository


def create_auth_interceptor(SessionDep):
    class Auth:
        async def get_user(self, db_session: SessionDep, token: Annotated[str | None, Cookie()] = None) -> User | None:
            """
            Retrieves the user from the authentication token.

            Parameters
            ----------
            db_session : Session
                The session to access the database.
            token : Annotated[str | None, Cookie()], optional
                The authentication token to use, by default None.

            Returns
            -------
            User | None
                The user from the authentication token, or None if the token is invalid.
            """
            auth_repository = AuthRepository(db_session)
            return await auth_repository.decode_authentication_token(token)

        async def redirect_auth(
                self,
                request: Request,
                db_session: SessionDep,
                token: Annotated[str | None, Cookie()] = None
        ):
            """
            Redirects users to the home page if they are not authenticated. Otherwise, add the user information
            in the request state.

            Parameters
            ----------
            request : Request
                The request information.
            db_session : Session
                The session to access the database.
            token : Annotated[str | None, Cookie()], optional
                The authentication token to use, by default None.
            """
            user = await self.get_user(db_session, token)

            if user is None:
                raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})

            request.state.user = user


        async def redirect_if_auth(
                self,
                request: Request,
                db_session: SessionDep,
                token: Annotated[str | None, Cookie()] = None
        ):
            """
            Redirects users to the home page if they are authenticated.

            Parameters
            ----------
            request : Request
                The request information.
            db_session : Session
                The session to access the database.
            token : Annotated[str | None, Cookie()], optional
                The authentication token to use, by default None.
            """
            user = await self.get_user(db_session, token)

            if user is not None:
                raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})


        async def unauthorized_auth(
                self,
                request: Request,
                db_session: SessionDep,
                token: Annotated[str | None, Cookie()] = None
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
            token : Annotated[str | None, Cookie()], optional
                The authentication token to use, by default None.
            """

            user = await self.get_user(db_session, token)

            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged.")

            request.state.user = user


        async def ws_unauthorized_auth(
                self,
                db_session: SessionDep,
                token: Annotated[str | None, Cookie()] = None
        ):
            """
            Throws an unauthorized exception if the user is not authenticated.

            Parameters
            ----------
            db_session : Session
                The session to access the database.
            token : Annotated[str | None, Cookie()], optional
                The authentication token to use, by default None.
            """

            user = await self.get_user(db_session, token)

            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged.")

    return Auth()
