# -*- coding: utf-8 -*-
"""

- Contributors
Elliann Marks <elian.markes@gmail.com>

- Version 01 - 20/03/2019 - Initial commit

- Documentation zenpy library
https://github.com/facetoe/zenpy
http://docs.facetoe.com.au/zenpy.html
"""

#libraries
import sys
import logging
import argparse
import time
from datetime import datetime
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, Comment, User
from contextlib import closing

class Usage:

    def __init__(self, zendesk):
        """
        Define arguments for use in class Zendesk
        """
        try:
            self._zendesk = zendesk
            #create private variables
            self.arguments = argparse.ArgumentParser()
            #subarguments to define action in zendesk
            self.action = self.arguments.add_subparsers(help='action in zendesk', required=True, dest='action')
            #create arguments
            self._createArguments()
            #search arguments
            self._searchArguments()
            #update arguments
            self._updateArguments()
            self._args = vars(self.arguments.parse_args())
            #set variables with values of the arguments
            self._initializeValues()

        except Exception as er:
            print("{} - {}".format(self.__class__.__name__, er))
            exit(1)

    def _initializeValues(self):
        try:
            self._zendesk._dictValues = {
                "description" : self._args.get("description"),
                "subject" : self._args.get("subject"),
                "tags" : self._args.get("tags"),
                "status" : self._args.get("status"),
                "assignee_id" : self._args.get("assignee_id"),
                "collaborator_ids" : self._args.get("collaborator_ids"),
                "assignee_email" : self._args.get("assignee_email"),
                "group_id" : self._args.get("group_id"),
                "organization_id" : self._args.get("organization_id"),
                "submitter_id" : self._args.get("submitter_id"),
                "ticket_form_id" : self._args.get("ticket_form_id"),
                "requester_id" : self._args.get("requester_id"),
                "requester" : self._args.get("requester"),
                "problem_id" : self._args.get("problem_id"),
                "macro_ids" : self._args.get("macro_ids"),
                "priority" : self._args.get("priority"),
                "comment" : self._args.get("comment")
            }
            self._zendesk._dictInternal = {
                "token": self._args.get("token"),
                "action": self._args.get("action"),
                "noVirtualenv": self._args.get("noVirtualenv"),
                "noDefaultToken": self._args.get("noDefaultToken"),
                "logFile": self._args.get("logFile"),
                "noKeepTags": self._args.get("noKeepTags"),
                "internalMacroID": self._args.get("internalMacroID"),
                "ticketID": self._args.get("ticketID"),
                "jobID": self._args.get("jobID"),
                "getID": self._args.get("get_id"),
            }
            self._zendesk._listValues = [
                "description", "subject", "tags", "assignee_id", "requester",
                "collaborator_ids", "assignee_email", "group_id", "organization_id", "submitter_id",
                "ticket_form_id", "requester_id", "comment", "status", "problem_id",
                "priority", "macro_ids",
            ]
            self._zendesk._listInternal = [
                "token", "action", "noVirtualenv", "noDefaultToken", "logFile",
                "upload", "internalMacroID", "ticketID", "noKeepTags", "getID",
                "jobID",
            ]
            self._zendesk._comment.public = self._args.get("private")
            self._zendesk._comment.uploads = self._args.get("upload")
            # check use together of the ticketid and jobid
            if self._zendesk._dictInternal["ticketID"] is not None and self._zendesk._dictInternal["jobID"] is not None:
                print("search: error: the following arguments can not be used together: -t, -j")
                exit(1)

        except Exception as er:
            print("{} - {}".format(self.__class__.__name__, er))
            exit(1)

    def _updateArguments(self):
        try:
            self.argUpdate = self.action.add_parser('update')
            self.argUpdate.add_argument('-t', dest='ticketID', help='ID of the ticket', metavar="ticketID",
                                        required=True, action="store")
            self.argUpdate.add_argument('--subject', dest='subject', help='subject of the comment',
                                        metavar="subject", action="store", default=None)
            self.argUpdate.add_argument('--comment', dest='comment', help='description of the comment',
                                        metavar="comment", action="store", default=None)
            self.argUpdate.add_argument('--private', dest='private', help='set private comment',
                                        action="store_false", default=True)
            self.argUpdate.add_argument('--tags', dest='tags', help='tags of the ticket',
                                        metavar="tags", required='--no-keep-tags' in sys.argv, action="store", default=None)
            self.argUpdate.add_argument('--status', dest='status', help='status of the ticket',
                                        metavar="status", action="store", default=None)
            self.argUpdate.add_argument('--macro-ids', dest='macro_ids', help='macro id to the ticket',
                                        metavar="macro_ids", action="store", default=None)
            self.argUpdate.add_argument('--assignee-id', dest='assignee_id', help='assignee ID of the ticket',
                                        metavar="assignee_id", action="store", default=None)
            self.argUpdate.add_argument('--collaborator-ids', dest='collaborator_ids', help='collaborator IDs of the ticket',
                                        metavar="collaborator_ids", action="store", default=None)
            self.argUpdate.add_argument('--assignee-email', dest='assignee_email', help='assignee email of the ticket',
                                        metavar="assignee_email", action="store", default=None)
            self.argUpdate.add_argument('--group-id', dest='group_id', help='group ID of the ticket',
                                        metavar="group_id", action="store", default=None)
            self.argUpdate.add_argument('--organization-id', dest='organization_id', help='organization ID of the ticket',
                                        metavar="organization_id", action="store", default=None)
            self.argUpdate.add_argument('--ticket-form-id', dest='ticket_form_id', help='ticket form ID of the ticket',
                                        metavar="ticket_form_id", action="store", default=None)
            self.argUpdate.add_argument('--submitter-id', dest='submitter_id', help='submitter ID of the ticket',
                                        metavar="submitter_id", action="store", default=None)
            self.argUpdate.add_argument('--requester-id', dest='requester_id', help='requester ID of the ticket',
                                        metavar="requester_id", action="store", default=None)
            self.argUpdate.add_argument('--requester', dest='requester', help='requester e-mail of the ticket',
                                        metavar="requester", action="store", default=None)
            self.argUpdate.add_argument('--problem-id', dest='problem_id', help='problem ID of the ticket',
                                        metavar="problem_id", action="store", default=None)
            self.argUpdate.add_argument('--priority', dest='priority', help='priority of the ticket',
                                        metavar="priority", action="store", default=None)
            self.argUpdate.add_argument('--no-keep-tags', dest='noKeepTags', help='this options clear the existing tags',
                                        action="store_true", default=None)
            self.argUpdate.add_argument('--upload', dest='upload', help='path of the file',
                                        metavar="path_file", action="store", default=None)
            self.argUpdate.add_argument('--macro-id-internal', dest='internalMacroID', help='use a internal macro to comment in ticket',
                                        metavar="internalMacroID", action="store", default=None)
            self.argUpdate.add_argument("--token", help="specific the token, only use if set --no-default-token",
                                        action="store", default=None, dest="token", metavar="token",
                                        required='--no-default-token' in sys.argv)
            self.argUpdate.add_argument("--no-virtualenv", help="no use virtualenv", action="store_true",
                                        default=None, dest="noVirtualenv")
            self.argUpdate.add_argument("--no-default-token", help="set for use the default token",
                                        default=None, action="store_true", dest="noDefaultToken")
            self.argUpdate.add_argument("--log-file", help="create log file in /tmp/zendesk_{date}.log",
                                        default=None, action="store_true", dest="logFile")

        except Exception as er:
            print("{} - {}".format(self.__class__.__name__, er))
            exit(1)

    def _searchArguments(self):
        try:
            self.argSearch = self.action.add_parser('search')
            self.argSearch.add_argument('-t', dest='ticketID', help='ID of the ticket', metavar="ticketID",
                                        required='-j' not in sys.argv, action="store", default=None)
            self.argSearch.add_argument('-j', dest='jobID', help='ID of the job', metavar="jobID",
                                        required='-t' not in sys.argv, action="store", default=None)
            self.argSearch.add_argument("--token", help="specific the token, only use if set --no-default-token",
                                        action="store", default=None, dest="token", metavar="token",
                                        required='--no-default-token' in sys.argv)
            self.argSearch.add_argument("--no-virtualenv", help="no use virtualenv", action="store_true",
                                        default=None, dest="noVirtualenv")
            self.argSearch.add_argument("--no-default-token", help="set for use the default token",
                                        default=None, action="store_true", dest="noDefaultToken")
            self.argSearch.add_argument("--log-file", help="create log file in /tmp/zendesk_{date}.log",
                                        default=None, action="store_true", dest="logFile")

        except Exception as er:
            print("{} - {}".format(self.__class__.__name__, er))
            exit(1)

    def _createArguments(self):
        try:
            self.argCreate = self.action.add_parser('create')
            self.argCreate.add_argument('--description', dest='description', help='description of the ticket',
                                        metavar="description", action="store", default=None)
            self.argCreate.add_argument('--subject', dest='subject', help='subject of the comment',
                                        metavar="subject", action="store", default=None)
            self.argCreate.add_argument('--get-id', dest='get_id', help='wait return ticket id',
                                        action="store_true", default=False)
            self.argCreate.add_argument('--tags', dest='tags', help='tags of the ticket',
                                        metavar="tags", action="store", default=None)
            self.argCreate.add_argument('--status', dest='status', help='status of the ticket',
                                        metavar="status", action="store", default=None)
            self.argCreate.add_argument('--macro-ids', dest='macro_ids', help='macro id to the ticket',
                                        metavar="macro_ids", action="store", default=None)
            self.argCreate.add_argument('--assignee-id', dest='assignee_id', help='assignee ID of the ticket',
                                        metavar="assignee_id", action="store", default=None)
            self.argCreate.add_argument('--collaborator-ids', dest='collaborator_ids',
                                        help='collaborator IDs of the ticket',
                                        metavar="collaborator_ids", action="store", default=None)
            self.argCreate.add_argument('--assignee-email', dest='assignee_email', help='assignee email of the ticket',
                                        metavar="assignee_email", action="store", default=None)
            self.argCreate.add_argument('--group-id', dest='group_id', help='group ID of the ticket',
                                        metavar="group_id", action="store", default=None)
            self.argCreate.add_argument('--organization-id', dest='organization_id',
                                        help='organization ID of the ticket',
                                        metavar="organization_id", action="store", default=None)
            self.argCreate.add_argument('--ticket-form-id', dest='ticket_form_id', help='ticket form ID of the ticket',
                                        metavar="ticket_form_id", action="store", default=None)
            self.argCreate.add_argument('--submitter-id', dest='submitter_id', help='submitter ID of the ticket',
                                        metavar="submitter_id", action="store", default=None)
            self.argCreate.add_argument('--requester-id', dest='requester_id', help='requester ID of the ticket',
                                        metavar="requester_id", action="store", default=None)
            self.argCreate.add_argument('--requester', dest='requester', help='requester e-mail of the ticket',
                                        metavar="requester", action="store", default=None)
            self.argCreate.add_argument('--problem-id', dest='problem_id', help='problem ID of the ticket',
                                        metavar="problem_id", action="store", default=None)
            self.argCreate.add_argument('--priority', dest='priority', help='priority of the ticket',
                                        metavar="priority", action="store", default=None)
            self.argCreate.add_argument('--macro-id-internal', dest='internalMacroID',
                                        help='use a internal macro to comment in ticket',
                                        metavar="internalMacroID", action="store", default=None)
            self.argCreate.add_argument("--token", help="specific the token, only use if set --no-default-token",
                                        action="store", default=None, dest="token", metavar="token",
                                        required='--no-default-token' in sys.argv)
            self.argCreate.add_argument("--no-virtualenv", help="no use virtualenv", action="store_true",
                                        default=None, dest="noVirtualenv")
            self.argCreate.add_argument("--no-default-token", help="set for use the default token",
                                        default=None, action="store_true", dest="noDefaultToken")
            self.argCreate.add_argument("--log-file", help="create log file in /tmp/zendesk_{date}.log",
                                        default=None, action="store_true", dest="logFile")

        except Exception as er:
            print("{} - {}".format(self.__class__.__name__, er))
            exit(1)

class ModuleLog:

	def __init__(self):
		"""
		Define values for create log instance
		"""
		try:
			#configuration logging
			self.logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
			self.logFile = "/tmp/zendesk_{}.log".format(str((datetime.now().date())))
			self.logLevel = logging.INFO
			#configuration log
			self.log = logging.getLogger(__name__)
			self.log.setLevel(self.logLevel)
			with closing(logging.FileHandler(self.logFile)) as self.logHandler:
				self.logHandler.setLevel(self.logLevel)
				self.logFormatter = logging.Formatter(self.logFormat)
				self.logHandler.setFormatter(self.logFormatter)
				self.log.addHandler(self.logHandler)

		except Exception as er:
			print("{} - {}".format(self.__class__.__name__, er))

class Zendesk:

    def __init__(self):
        self._log = None
        self._token = "XXXXX"
        self._subdomain = "example"
        self._email = "apizendesk@example.com"
        #fields for comments in ticket
        self._comment = Comment
        self._comment.public = None
        self._comment.body = None
        self._comment.uploads = None
        #fields for create a ticket
        self._dictValues = dict()
        self._listValues = list()
        #fields of the application
        self._dictInternal = dict()
        self._listInternal = list()
        #objects
        self._updateObject = None
        self._searchObject = None
        self._createObject = None
        #LF and CRLF
        self._crlf = b'\r\n'
        self._lf = b'\n'

    #return object with connection of the zendesk
    @property
    def connectZendesk(self):
        """

        :return:
        """
        try:
            self._credentials = {
                "email" : self._email,
                "token" : self._token,
                "subdomain" : self._subdomain
            }
            return Zenpy(**self._credentials)

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    def executeAction(self):
        try:
            if self._dictInternal["noDefaultToken"] is True and self._dictInternal["token"] is not None:
                self._token = self._dictInternal["token"]
            if self._dictInternal["action"] == "create":
                self.resultCreate = self.createTicket()
                if self._dictInternal['getID'] is True:
                    print(self.jobStatus(self.resultCreate.id))
                else:
                    print(self.resultCreate.id)

            elif self._dictInternal["action"] == "update":
                self._updateObject = self.searchID()
                for self.item in self._listValues:
                    if self._dictValues[self.item] is not None and self._dictValues[self.item] is not False:
                        if self._dictInternal["noKeepTags"] is not True and self.item == "tags":
                            self._updateObject.tags.append(self._dictValues["tags"])
                        elif self.item == "requester" and self._dictValues[self.item] is not None:
                            self._updateObject.requester = User(name=self._dictValues[self.item].split("@")[0], email=self._dictValues[self.item])
                        elif self.item == "comment" and self._dictValues[self.item] is not None:
                            self.commentTicket()
                        elif self.item == "macro_ids" and self._dictValues[self.item] is not None:
                            self.updateTicket(self.macroID().ticket)
                        else:
                            print(self.item)
                            setattr(self._updateObject, self.item, self._dictValues[self.item])
                self.updateTicket(self._updateObject)
            elif self._dictInternal["action"] == "search":
                if self._dictInternal["ticketID"] is not None:
                    self._searchObject = self.searchID()
                    print(self._searchObject.to_dict())
                elif self._dictInternal["jobID"] is not None:
                    print(self.jobStatus(self._dictInternal["jobID"]))

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    # create a ticket, necessary define the subject and description
    def createTicket(self):
        """

        :return:
        """
        try:
            if self._dictValues["subject"]is not None and self._dictValues["description"] is not None:
                print("Ok")
                if self._dictValues['requester'] is not None:
                    self.createTicketObject = self.connectZendesk.tickets.create(
                        [Ticket(subject=self._dictValues["subject"], description=self._dictValues["description"],
                                assignee_id=self._dictValues["assignee_id"], group_id=self._dictValues["group_id"],
                                organization_id=self._dictValues["organization_id"],
                                priority=self._dictValues["priority"],
                                problem_id=self._dictValues["problem_id"], status=self._dictValues["status"],
                                tags=self._dictValues["tags"],
                                requester=User(name=self._dictValues['requester'].split("@")[0], email=self._dictValues['requester']),
                                submitter_id=self._dictValues["submitter_id"],
                                ticket_form_id=self._dictValues["ticket_form_id"],
                                assignee_email=self._dictValues["assignee_email"],
                                collaborator_ids=self._dictValues["collaborator_ids"])])
                else:
                    self.createTicketObject = self.connectZendesk.tickets.create(
                        [Ticket(subject=self._dictValues["subject"], description=self._dictValues["description"],
                                assignee_id=self._dictValues["assignee_id"], group_id=self._dictValues["group_id"],
                                organization_id=self._dictValues["organization_id"], priority=self._dictValues["priority"],
                                problem_id=self._dictValues["problem_id"], status=self._dictValues["status"], tags=self._dictValues["tags"],
                                requester_id=self._dictValues["requester_id"],
                                submitter_id=self._dictValues["submitter_id"], ticket_form_id=self._dictValues["ticket_form_id"],
                                assignee_email=self._dictValues["assignee_email"],
                                collaborator_ids=self._dictValues["collaborator_ids"])])
                return self.createTicketObject
            else:
                self._log.error("{} - {}".format(self.__class__.__name__, "Object description or subject empty"))
                return False

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    #update a ticket
    def jobStatus(self, resultJobID):
        try:
            self.countStatus = 0
            self.resultJobID = resultJobID
            while self.countStatus <= 10:
                time.sleep(5)
                self.resultJobStatus = self.connectZendesk.job_status(id=self.resultJobID)
                if self.resultJobStatus.status == "completed":
                    return self.resultJobStatus.results[0].id
                self.countStatus += 1

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    #update a ticket
    def updateTicket(self, updateObject):
        """

        :param updateObject:
        :return:
        """
        try:
            self.updateObject = updateObject
            return self.connectZendesk.tickets.update(self.updateObject)

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    #id search
    def searchID(self):
        try:
            return self.connectZendesk.tickets(id=self._dictInternal['ticketID'])

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    #id search
    def macroID(self):
        try:
            return self.connectZendesk.tickets.show_macro_effect(self._updateObject, self._dictValues['macro_ids'])

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    def commentTicket(self):
        """

        :return:
        """
        try:
            self._comment.body = self._dictValues['comment']
            if self._comment.uploads is not None:
                self._updateObject.comment = Comment(body=self._comment.body, public=self._comment.public, uploads=[self.uploadFile(self._comment.uploads).token])
            else:
                self._updateObject.comment = Comment(body=self._comment.body, public=self._comment.public)

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    def uploadFile(self, uploadFile):
        """

        :param uploadFile:
        :return:
        """
        try:
            self.uploadFile = uploadFile
            self.convertLFtoCRLF(self.uploadFile)
            return self.connectZendesk.attachments.upload(self.uploadFile)

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

    def convertLFtoCRLF(self, convertFile):
        try:
            self.convertFile = convertFile
            # open file
            with open(self.convertFile, 'rb') as convertFileOpen:
                self.convertContent = convertFileOpen.read()
            # convert LF to CRLF
            self.convertContent = self.convertContent.replace(self._lf, self._crlf)
            # save file
            with open(self.convertFile, 'wb') as convertFileOpen:
                convertFileOpen.write(self.convertContent)

        except Exception as er:
            if self._log is not None:
                self._log.error("{} - {}".format(self.__class__.__name__, er))
            else:
                print("{} - {}".format(self.__class__.__name__, er))
            return False

def main():
    try:
        zendesk = Zendesk()
        usage = Usage(zendesk)
        if zendesk._dictInternal["logFile"] is not None:
            moduleLog = ModuleLog()
            zendesk._log = moduleLog.log
            print("Log - '{}'".format(moduleLog.logFile))
        zendesk.executeAction()

    except Exception as er:
        print("{} - {}".format(__name__, er))
        exit(1)

if __name__ == '__main__':
    main()
