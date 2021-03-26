class DFContext:

    """
    "message": "Webhook call failed. Error: [ResourceName error] Path 'name' does not match template 
    'projects/{project_id=*}/locations/{location_id=*}/agent/environments/{environment_id=*}/users/{user_id=*}/sessions/{session_id=*}/contexts/{context_id=*}'.."
    """

    def addContext(self, parameters, session):
        output = []

        context = {}
        context["name"] = f'{session}/contexts/__usuario__'
        context["lifespanCount"] = 8
        context["parameters"] = parameters

        output.append(context)
        return output
