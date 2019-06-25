# Dataviews.py
#

import json

from .Dataview.Dataview import Dataview
from .Dataview.Datagroup import Datagroup

import requests


class Dataviews(object):
    """
    Client for interacting with Dataviews
    """

    def __init__(self, client):
        """
        Initiliizes the dataviews client
        :param client: This is the base client that is used to make the callss
        """
        self.__baseClient = client
        self.__setPathAndQueryTemplates()

    def postDataview(self, namespace_id, dataview):
        """Tells Sds Service to create a dataview based on local 'dataview'
            or get if existing dataview matches
        :param namespace_id: namespace to work against
        :param dataview: dataview defintion.  Dataview object expected
        :return: Retreived dataview as Dataview object
        """
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError

        response = requests.post(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview.Id),
            data=dataview.toJson(),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to create dataview, {dataview.Id}.")

        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview

    def putDataview(self, namespace_id, dataview):
        """Tells Sds Service to update a dataview based on local 'dataview'
        :param namespace_id: namespace to work against
        :param dataview: dataview defintion.  Dataview object expected
        :return: Retreived dataview as Dataview object
        """
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError
        response = requests.put(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview.Id),
            data=dataview.toJson(),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to update dataview, {dataview.Id}.")

        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview

    def deleteDataview(self, namespace_id, dataview_id):
        """
        Tells Sds Service to delete a dataview based on 'dataview_id'
        :param namespace_id: namespace to work against
        :param dataview_id:  id of dataview to delete
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        response = requests.delete(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to delete dataview, {dataview_id}.")

        response.close()
        return

    def getDataview(self, namespace_id, dataview_id):
        """
        Retrieves the dataview specified by 'dataview_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id:  id of dataview to get
        :return: Retreived dataview as Dataview object
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        response = requests.get(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get dataview, {dataview_id}.")

        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview

    def getDataviews(self, namespace_id, skip=0, count=100):
        """
        Retrieves all of the dataviews from Sds Service
        :param namespace_id: namespace to work against
        :param skip: Number of dataviews to skip
        :param count: Number of dataviews to return
        :return: array of dataviews
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataviewsPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(response, "Failed to get dataviews.")

        dataviews = json.loads(response.content)

        results = []
        for t in dataviews:
            results.append(Dataview.fromJson(t))
        response.close()
        return results

    def getDatagroups(self, namespace_id, dataview_id, skip=0,
                      count=100, returnAsDynamicObject=False):
        """
        Retrieves all of the datagroups from the specified dataview from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param skip: Number of datagroups to skip
        :param count: Number of datagroups to return
        :param returnAsDynamicObject: returns the collection as dynamic object
                rather than a list of dataviews.  Added because the automated
                tests were failing.  Boolean
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__datagroupPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get datagroups for dataview, {dataview_id}.")

        datagroups = json.loads(response.content)

        if returnAsDynamicObject:
            return datagroups

        results = []
        for datagroup in datagroups['DataGroups']:
            results.append(Datagroup.fromJson(datagroup))
        response.close()

        return results

    def getDatagroup(self, namespace_id, dataview_id, datagroup_id):
        """
        Retrieves a datagroupby 'datagroup_id' from the specified
            dataview from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param datagroup_id: datagroup to retrieve
        :return: the asked for Datagroup
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__getDatagroup.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id,
                datagroup_id=datagroup_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get datagroup, {datagroup_id},"
                      " for dataview, {dataview_id}.")

        datagroup = Datagroup.fromJson(json.loads(response.content))
        return datagroup

        # needs other parameters with smart
    def getDataviewPreview(self, namespace_id, dataview_id, startIndex=None,
                           endIndex=None, interval=None, form=None, count=None,
                           value_class=None):
        """
        Retrieves the dataviewpreview of the 'dataview_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param startIndex: start index
        :param endIndex:  end index
        :param interval: space between values
        :param form: form definition
        :param count: number of values to return
        :param value_class: Use this to auto format the data into the defined
            type.  The tpye is expected to have a fromJson method that takes
            a dynamicObject and converts it into the defined type.
          Otherwise you get a dynamic object
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        params = {"startIndex": startIndex, "endIndex": endIndex,
                  "interval": interval, "form": form, "count": count}
        response = requests.get(
            self.__getDataviewPreview.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id),
            headers=self.__baseClient.sdsHeaders(),
            params=params
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get dataview preview"
            " for dataview, {dataview_id}.")

        if form is not None:
            content = response.text
        else:
            content = json.loads(response.content)
        response.close()

        if value_class is None:
            return (content)
        return value_class.fromJson(content)

    def getDataInterpolated(self, namespace_id, dataview_id, skip=None,
                            count=None, form=None, sessionId=None,
                            value_class=None):
        """
        Retrieves the dataviewpreview of the 'dataview_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param skip: number of values to skip
        :param count: number of values to return
        :param form: form definition
        :param sessionId: used so you can return to a call to get more data if
             you need to page
        :param value_class: Use this to auto format the data into the defined
            type.  The tpye is expected to have a fromJson method that takes a
            dynamicObject and converts it into the defined type.
          Otherwise you get a dynamic object
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        params = {"count": count, "skip": skip, "form": form,
                  "sessionId": sessionId}
        response = requests.get(
            self.__getDataInterpolated.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id),
            headers=self.__baseClient.sdsHeaders(),
            params=params,
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get dataview data interpolated"
                      " for dataview, {dataview_id}.")

        if form is not None:
            return response.text

        content = json.loads(response.content)
        response.close()

        if value_class is None:
            return (content)
        return value_class.fromJson(content)

    def __setPathAndQueryTemplates(self):
        """
        Internal  Sets the needed URLS
        :return:
        """
        self.__basePath = self.__baseClient.uri_API + \
            "/Tenants/{tenant_id}/Namespaces/{namespace_id}"

        self.__dataviewsPath = self.__basePath + "/Dataviews"
        self.__dataviewPath = self.__dataviewsPath + "/{dataview_id}"
        self.__datagroupPath = self.__dataviewPath + "/Datagroups"
        self.__getDatagroup = self.__datagroupPath + "/{datagroup_id}"
        self.__getDataviewPreview = self.__dataviewPath + \
            "/preview/interpolated"
        self.__getDataInterpolated = self.__dataviewPath + "/data/interpolated"
