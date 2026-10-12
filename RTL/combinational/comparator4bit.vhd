library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity comparator4bit is
    Port (
        A         : in  STD_LOGIC_VECTOR(3 downto 0);
        B         : in  STD_LOGIC_VECTOR(3 downto 0);
        A_GREATER : out STD_LOGIC;
        A_EQUAL   : out STD_LOGIC;
        A_LESS    : out STD_LOGIC
    );
end comparator4bit;

architecture Behavioral of comparator4bit is
begin

    A_GREATER <= '1' when unsigned(A) > unsigned(B) else '0';

    A_EQUAL <= '1' when unsigned(A) = unsigned(B) else '0';

    A_LESS <= '1' when unsigned(A) < unsigned(B) else '0';

end Behavioral;