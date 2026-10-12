library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mux is
    Port (
        A : in  STD_LOGIC;
        B : in  STD_LOGIC;
        S : in  STD_LOGIC;
        Y : out STD_LOGIC
    );
end mux;

architecture Behavioral of mux is
begin

    Y <= A when S = '0' else B;

end Behavioral;