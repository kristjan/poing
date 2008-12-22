require 'net/http'
require 'uri'

POINGER = 'Me'
POINGEE = 'Them'

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
                 :poinger => POINGER, :poingee => POINGEE
    ERROR != poing.body
  end

  TWELVE_HOURS = (12*60*60).to_f
  ONE_MINUTE = 60.0
  TOTAL_DECAY = ONE_MINUTE
  def alpha(time)
    alpha = ([1 - (time / TOTAL_DECAY), 0].max * 255).to_i
  end

  def color(base, time)
    return black if time < 0
    rgb(*(base + [alpha(time)]))
  end

  MY_COLOR = [255, 0, 0]
  THEIR_COLOR = [0, 255, 0]

  def update_poinger
    @my_dot.fill = color(MY_COLOR, @my_poing)
    @their_dot.fill = color(THEIR_COLOR, @their_poing)
  end

  @my_dot = oval :radius => 10, :top => 5, :left => 5
  @their_dot = oval :radius => 10, :top => 5, :left => 30

  animate do
    update_poinger
  end

  click do
    poing
    @their_poing = poinged(POINGER, POINGEE)
  end

  Thread.new do
    loop do
      @their_poing = poinged(POINGER, POINGEE)
      @my_poing = poinged(POINGEE, POINGER)
      sleep 5
    end
  end
end