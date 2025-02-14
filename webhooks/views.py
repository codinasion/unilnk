from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import git
import os
from . import models
from .validate_github_auth import ValidateGithubAuth


class ServerUpdateView(APIView):
    """
    Update server code on push event
    """

    def post(self, request):
        try:
            # Validate request
            if not ValidateGithubAuth(request):
                return Response(
                    {"message": "Not a valid request !!!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get event type
            event = request.META.get("HTTP_X_GITHUB_EVENT")

            if event == "ping":
                return Response(status=status.HTTP_200_OK)

            elif event == "push":
                try:
                    # Perform "git pull" to update the server code
                    repo = git.Repo(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        search_parent_directories=True,
                    )
                    origin = repo.remotes.origin
                    origin.pull()

                    # Add server update status to database
                    server_update = models.ServerUpdateModel()
                    server_update.server_update_status = True
                    server_update.save()

                    return Response(
                        {"message": "Successfully updated the server code !!!"},
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    print(str(e))

                    # Add server update status to database
                    server_update = models.ServerUpdateModel()
                    server_update.server_update_status = False
                    server_update.server_update_error = str(e)
                    server_update.save()

                    return Response(
                        {"message": "Error updating server code :("},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            # In case we receive an event that's not "ping" or "push"
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "Error updating server code :("},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
