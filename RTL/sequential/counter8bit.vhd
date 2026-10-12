library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity counter8bit is
    Port (
        CLK   : in  STD_LOGIC;
        RESET : in  STD_LOGIC;
        EN    : in  STD_LOGIC;
        COUNT : out STD_LOGIC_VECTOR(7 downto 0)
    );
end counter8bit;

architecture Behavioral of counter8bit is

    signal count_reg : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');

begin

    process(CLK)
    begin
        if rising_edge(CLK) then
            if RESET = '1' then
                count_reg <= (others => '0');
            elsif EN = '1' then
                count_reg <= count_reg + 1;
            end if;
        end if;
    end process;

    COUNT <= count_reg;

end Behavioral;