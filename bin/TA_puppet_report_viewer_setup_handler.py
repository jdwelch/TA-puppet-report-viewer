import splunk.admin as admin
import splunk.entity as en
# import your required python modules

'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
Description:  This skeleton python script handles the parameters in the configuration page.

      handleList method: lists configurable parameters in the configuration page
      corresponds to handleractions = list in restmap.conf

      handleEdit method: controls the parameters and saves the values 
      corresponds to handleractions = edit in restmap.conf

'''

class ConfigApp(admin.MConfigHandler):
  '''
  Set up supported arguments
  '''
  def setup(self):
    if self.requestedAction == admin.ACTION_EDIT:
      for arg in ['field_1', 'field_2_boolean', 'field_3']:
        self.supportedArgs.addOptArg(arg)
        
  '''
  Read the initial values of the parameters from the custom file
      inputs.conf, and write them to the setup page. 

  If the app has never been set up,
      uses .../app_name/default/inputs.conf. 

  If app has been set up, looks at 
      .../local/inputs.conf first, then looks at 
  .../default/inputs.conf only if there is no value for a field in
      .../local/inputs.conf

  For boolean fields, may need to switch the true/false setting.

  For text fields, if the conf file says None, set to the empty string.
  '''

  def handleList(self, confInfo):
    confDict = self.readConf("inputs")
    if None != confDict:
      for stanza, settings in confDict.items():
        for key, val in settings.items():
          if key in ['field_2_boolean']:
            if int(val) == 0:
              val = '0'
            else:
              val = '1'
          if key in ['field_4_boolean']:
            if int(val) == 0:
              val = '0'
            else:
              val = '1'
          if key in ['field_1'] and val in [None, '']:
            val = ''
          confInfo[stanza].append(key, val)
          
  '''
  After user clicks Save on setup page, take updated parameters,
  normalize them, and save them somewhere
  '''
  def handleEdit(self, confInfo):
    name = self.callerArgs.id
    args = self.callerArgs
    
    if int(self.callerArgs.data['field_4_boolean'][0]) == 1:
      self.callerArgs.data['field_4_boolean'][0] = '0'
    else:
      self.callerArgs.data['field_4_boolean'][0] = '1'

    if int(self.callerArgs.data['field_3'][0]) < 60:
      self.callerArgs.data['field_3'][0] = '60'
        
    if int(self.callerArgs.data['field_2_boolean'][0]) == 1:
      self.callerArgs.data['field_2_boolean'][0] = '0'
    else:
      self.callerArgs.data['field_2_boolean'][0] = '1'
    
    if self.callerArgs.data['field_1'][0] in [None, '']:
      self.callerArgs.data['field_1'][0] = ''  

        
    '''
    Since we are using a conf file to store parameters, 
write them to the [setupentity] stanza
    in app_name/local/inputs.conf  
    '''
        
    self.writeConf('inputs', 'setupentity', self.callerArgs.data)
      
# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)