#!/usr/bin/env python

import boto3
import json
import os
from github import Github, GithubException, UnknownObjectException

class gh_auth():

    def __init__(self, **kwargs):
        try:
            self.token_path = kwargs['TokenPath']
            self.token = self.get_github_pat()
        except KeyError:
            self.token = os.getenv('GITHUB_PAT')

        self.org_name = kwargs.get('OrgName', '2uinc')
        self.user_name = kwargs.get('UserName', 'the-real-cphillips')
        self.login = self.login()
        self.org = self.org()


    def get_github_pat(self):
        """ Retreive Github Token from AWS Secrets Manager """
        
        client = boto3.client('secretsmanager', region_name='us-west-2')
        response = client.get_secret_value(
                SecretId=self.token_path
                )
        json_data = json.loads(response['SecretString'])
        token = json_data['token:general_purpose']
        return token


    def login(self):
        """
        Does the "login" using the PAT Token
        """
        git = Github(self.token)
        return git
    
    
    def org(self):
        """
        Gets the Organization
        """
        org = self.login.get_organization(self.org_name)
        return org

    def user(self):
        """
        Gets a User
        """
        user = self.login.get_user(self.user_name)
        return user
