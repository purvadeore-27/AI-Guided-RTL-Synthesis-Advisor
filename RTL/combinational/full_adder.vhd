library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity full_adder is
    Port (
        A     : in  STD_LOGIC;
        B     : in  STD_LOGIC;
        C     : in  STD_LOGIC;
        SUM   : out STD_LOGIC;
        Carry : out STD_LOGIC
    );
end full_adder;

architecture Behavioral of full_adder is
begin

    SUM   <= A XOR B XOR C;
    Carry <= (A AND B) OR (B AND C) OR (A AND C);

end Behavioral;