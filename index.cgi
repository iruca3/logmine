#!/usr/local/bin/ruby
# -*- coding: utf-8 -*-
#===============================================================================
# Generate the analyzed log from 'server.log' of minecraft.
#===============================================================================

require 'cgi'
require 'time'
require './User.rb'
require './LogParser.rb'
require './config.rb'

print "Content-type: text/html\n\n"

#-------------------------------------------------------------------------------
# Defines
#-------------------------------------------------------------------------------

$VERSION = "1.0.1"
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


#----  parse log
parser = LogParser.new( log_data )
parser.parse()
users = parser.getUsers()
types = parser.getTypes()

#----  sort by the sum of playtime and output playtime data
print '<html><head><title>Minecraft PlayTime</title></head>'
print '<body>'
print '<table border="1"><thead><tr><th>Type</th><th>Count</th></thead>'
print '<tbody>'
types.sort { |a, b| b[1] <=> a[1] }.each do |type, count|
  print '<tr>'
  print "  <td>#{type}</td>"
  print "  <td>#{count}</td>"
  print '</tr>'

end
print '</tbody></table>'

print '<hr>'

print '<table border="1"><thead><tr><th>User</th><th>TotalPlayTime</th><th>AveragePlayTime</th></tr></thead>'
print '<tbody>'
users.sort { |a, b| b[1].getTotalPlayTime().to_i <=> a[1].getTotalPlayTime().to_i }.each do |key, user|
  total_play_time = Time.at( user.getTotalPlayTime() ).gmtime.strftime( '%H:%M:%S' )
  average_play_time = Time.at( user.getAveragePlayTime() ).gmtime.strftime( '%H:%M:%S' )

  print '<tr>'
  print '  <td>' + user.name + '</td>'
  print '  <td>' + total_play_time + '</td>'
  print '  <td>' + average_play_time + '</td>'
  print '</tr>'

end
print '</tbody></table></body></html>'

exit
