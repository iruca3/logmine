#-------------------------------------------------------------------------------
# LogParser class
#-------------------------------------------------------------------------------

class LogParser
  @log_data
  @users
  @types

  def initialize( log_data )
    @log_data = log_data
  
  end

  def parse
    @users = Hash.new
    @types = Hash.new

    log_lines = @log_data.split( "\n" )
    log_lines.each do |line|
      time = Time.parse( line[ 0, 19 ], 0 ) rescue nil
      if time == nil
        next

      end

      line[/\[(.*?)\]/]
      log_type = $1
      log_line_prefix = 'yyyy-mm-dd HH:MM:SS [' + log_type + '] '
      line = line[ log_line_prefix.length .. -1 ]

      #----  analyze log type
      @types[ log_type ] = 0 if @types[ log_type ] == nil
      @types[ log_type ] += 1

      #----  analyze contents
      if line == 'Stopping server'
        # do something
        
      elsif line =~ /^Starting/
        # do something
        
      elsif line =~ /^(.*?) joined/
        joined_user = $1
        @users[ joined_user ] = User.new( joined_user ) if @users[ joined_user ] == nil
        @users[ joined_user ].startPlay( time )

      elsif line =~ /^(.*?) lost connection/
        leaved_user = $1
        @users[ leaved_user ].stopPlay( time ) if @users[ leaved_user ] != nil

      elsif line =~ /^<(.*?)> (.+)/
        chat_user     = $1
        chat_contents = $2
        # do something
        
      end

    end

    return true

  end
  
  def getUsers
    return @users
  end

  def getTypes
    return @types
  end

end
