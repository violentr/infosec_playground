require 'msf/core'

class Metasploit3 < Msf::Auxiliary
  include Msf::Exploit::Remote::Tcp
  include Msf::Auxiliary::Scanner

  def initialize
    super( 'Name' => "My Custom TCP scan",
           'Version' => "$Revision: 1 $",
           'Description' => "Simple TCP port scanner",
           'Author' => 'violentr',
           'License' =>   MSF_LICENSE
         )
   register_options(
       [Opt::RPORT(10000)], self.class)
    end

   def run_host(ip)
      connect()
      sock.puts("Hello Server")
      data = sock.recv(1024)
      print_status("Received #{data} from #{ip}")
      disconnect()
   end

end
