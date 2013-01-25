#-------------------------------------------------------------------------------
# User class
#-------------------------------------------------------------------------------

class User
  @name
  @playtime_logs
  @start_time
  @stop_time

  def initialize( name )
    @name = name
    @playtime_logs = Array.new
  
  end
  
  def startPlay( start_time )
    @start_time = start_time

  end
  
  def stopPlay( stop_time )
    @stop_time = stop_time

    playtime_log = Hash.new
    playtime_log['start'] = @start_time
    playtime_log['stop']  = @stop_time
    @playtime_logs.push( playtime_log )

  end
  
  def getTotalPlayTime
    total_time = 0
    @playtime_logs.each { |log|
      total_time = total_time + ( log['stop'] - log['start'] )

    }
    return total_time

  end
  
  def getAveragePlayTime
    return getTotalPlayTime() / @playtime_logs.size

  end

  attr_accessor :name

end
