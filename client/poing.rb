require 'net/http'
require 'uri'

ME   = {:name => 'Me', :color => [0, 255, 0]}
THEM = {:name => 'Them',    :color => [0, 0, 255]}

HOST = 'poingme.appspot.com'
ACTION = '/poing'
GET_PARAMS = ACTION + "?poinger=%s&poingee=%s"
POST_URL = 'http://' + HOST + ACTION

ERROR = "ERROR"

Shoes.app :width => 55, :height => 30, :resizeable => false do
  background "#FFF"

  @their_poing = @my_poing = -1

  def poinged(from, to)
    poing = Net::HTTP.get HOST, GET_PARAMS % [from, to]
    poing = -1 if poing.empty? || ERROR == poing
    debug "Getting poing for #{from} -> #{to}: #{poing.to_i}"
    poing.to_i
  end

  def poing
    poing = Net::HTTP.post_form URI.parse(POST_URL),
                 :poinger => ME[:name], :poingee => THEM[:name]
    ERROR != poing.body
  end

  TWELVE_HOURS = (12*60*60).to_f
  def alpha(time)
    alpha = ([1 - (time / TWELVE_HOURS), 0].max * 255).to_i
  end

  def color(base, time)
    return black if time < 0
    rgb(*(base + [alpha(time)]))
  end

  def update_dots
    @my_dot.fill = color(ME[:color], @my_poing)
    @their_dot.fill = color(THEM[:color], @their_poing)
  end

  @my_dot = oval :radius => 10, :top => 5, :left => 5
  @their_dot = oval :radius => 10, :top => 5, :left => 30

  animate do
    update_dots
  end

  click do
    Thread.new do
      poing
      @their_poing = 0
    end
  end

  Thread.new do
    loop do
      @their_poing = poinged(ME[:name], THEM[:name])
      @my_poing    = poinged(THEM[:name], ME[:name])
      sleep 5
    end
  end
end