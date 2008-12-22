require 'net/http'
require 'uri'

ME   = {:name => 'Me', :color => [0, 255, 0]}
THEM = {:name => 'Them',    :color => [0, 0, 255]}

HOST = 'poingme.appspot.com'
ACTION = '/poing'
GET_PARAMS = ACTION + "?poinger=%s&poingee=%s"
POST_URL = 'http://' + HOST + ACTION

ERROR = "ERROR"


Shoes.app :width => 55, :height => 30, :resizable => false do
  background "#FFF"

  @their_poing = @my_poing = -1

  def update_poings
    @their_poing = poinged(ME[:name], THEM[:name])
    @my_poing    = poinged(THEM[:name], ME[:name])
  end

  def poinged(from, to)
    poing = Net::HTTP.get HOST, GET_PARAMS % [from, to]
    poing = -1 if poing.empty? || ERROR == poing
    poing.to_i
  end

  def poing
    poing = Net::HTTP.post_form URI.parse(POST_URL),
                 :poinger => ME[:name], :poingee => THEM[:name]
    ERROR != poing.body
  end

  class ::Fixnum
    def second
      self
    end
    alias :seconds :second

    def minute
      self*60
    end
    alias :minutes :minute

    def hour
      self*3600
    end
    alias :hours :hour
  end

  INFINITY = 1.0/0
  ALPHAS = [
            [0, 255],
            [1.minute, 127],
            [10.minutes, 63],
            [1.hour, 31],
            [6.hours, 15],
            [12.hours, 0],
            [INFINITY, 0]
           ]
  def alpha(time)
    index = 0
    begin
      break if (ALPHAS[index].first...ALPHAS[index+1].first).include?(time)
      index += 1
    end while ALPHAS[index].first < INFINITY
    val = ALPHAS[index].last
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
    @their_poing = 0
    poing
  end

  every 5.seconds do
    update_poings
  end
end