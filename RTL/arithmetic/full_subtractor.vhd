library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity full_subtractor is
    Port (
        A        : in  STD_LOGIC;
        B        : in  STD_LOGIC;
        Bin      : in  STD_LOGIC;
        DIFFERENCE : out STD_LOGIC;
        BORROW   : out STD_LOGIC
    );
end full_subtractor;

architecture Behavioral of full_subtractor is
begin

    DIFFERENCE <= A XOR B XOR Bin;

    BORROW <= ((NOT A) AND B) OR
              ((NOT (A XOR B)) AND Bin);

end Behavioral;