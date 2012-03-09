#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
#===============================================================================
# Generate the analyzed log from 'server.log' of minecraft.
#===============================================================================

require 'cgi'
require 'time'
require './User.rb'
require './config.rb'


#-------------------------------------------------------------------------------
# Defines
#-------------------------------------------------------------------------------

$VERSION = "1.0.0"
$QUERY   = CGI.new

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

if $METHOD == 1
  file_handle = open( $PATH_SERVERLOG )
  log_data = File.read( file_handle, :encoding => $ENCODING_SERVERLOG )
  file_handle.close

elsif $METHOD == 2
  filename  = $QUERY['file'].local_path
  dot_pos   = filename.rindex( "." )
  prefix    = filename[ dot_pos+1 .. filename.length ]
  if prefix != "log"
    #----  invalid extension
    exit
  
  end
  log_data = $QUERY['file'].read

else
  #----  invalid method
  exit

end


#----  prepare variables
users = Hash.new              # user object


#----  parse log
log_lines = log_data.split( "\n" )
log_lines.each { |line|
  time = Time.parse( line[ 0, 19 ], 0 ) rescue nil
  if time == nil
    next

  end
  line[/\[(.*?)\]/]
  log_type = $1
  
  line = line[ ( 23 + log_type.length ) .. -1 ]
  
  #----  analyze contents
  if line == "Stopping server"
    

  elsif line =~ /^Starting/
    

  elsif line =~ /^(.*?) joined/
    joined_user = $1
    users[ joined_user ] = User.new( joined_user ) if users[ joined_user ] == nil
    users[ joined_user ].startPlay( time )

  elsif line =~ /^(.*?) lost connection/
    leaved_user = $1
    users[ leaved_user ].stopPlay( time ) if users[ leaved_user ] != nil

  elsif line =~ /^<(.*?)> (.+)/
    chat_user     = $1
    chat_contents = $2

  end

}


#----  sort by the sum of playtime and output playtime data
print "Content-type: text/plain\n\n"
print "User,TotalPlayTime,AveragePlayTime\n"
users.sort { |a, b| b[1].getTotalPlayTime().to_i <=> a[1].getTotalPlayTime().to_i }.each { |key, user|
  print user.name + "," + user.getTotalPlayTime().to_s + "," + user.getAveragePlayTime().to_s + "\n"

}

exit