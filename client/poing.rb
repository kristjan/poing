require 'net/http'
require 'uri'

POINGER = 'Me'
POINGEE = 'Them'

HOST = 'poingme.appspot.com'
ACTION = '/poing'
PARAMS = "?poinger=#{POINGER}&poingee=#{POINGEE}"
GET_ACTION = ACTION + PARAMS
POST_URL = 'http://' + HOST + ACTION

Shoes.app do
  stack do
    button "Fetch" do
      poing = Net::HTTP.get HOST, GET_ACTION
      alert(poing)
    end
    button "Poing" do
      poing = Net::HTTP.post_form URI.parse(POST_URL),
                   :poinger => POINGER, :poingee => POINGEE
      alert(poing.body)
    end
  end
end