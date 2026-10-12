library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity half_subtractor is
    Port (
        A          : in  STD_LOGIC;
        B          : in  STD_LOGIC;
        DIFFERENCE : out STD_LOGIC;
        BORROW     : out STD_LOGIC
    );
end half_subtractor;

architecture Behavioral of half_subtractor is
begin
    DIFFERENCE <= A XOR B;
    BORROW     <= (NOT A) AND B;
end Behavioral;