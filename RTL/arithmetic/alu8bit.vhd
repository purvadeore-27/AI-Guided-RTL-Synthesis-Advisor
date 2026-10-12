library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity alu8bit is
    Port (
        A         : in  STD_LOGIC_VECTOR(7 downto 0);
        B         : in  STD_LOGIC_VECTOR(7 downto 0);
        SEL       : in  STD_LOGIC_VECTOR(2 downto 0);
        RESULT    : out STD_LOGIC_VECTOR(7 downto 0);
        CARRY_OUT : out STD_LOGIC;
        ZERO      : out STD_LOGIC
    );
end alu8bit;

architecture Behavioral of alu8bit is
    signal RES  : STD_LOGIC_VECTOR(7 downto 0);
    signal TEMP : UNSIGNED(8 downto 0);
begin

    process(A, B, SEL)
    begin
        RES  <= (others => '0');
        TEMP <= (others => '0');
        CARRY_OUT <= '0';

        case SEL is

            -- Addition
            when "000" =>
                TEMP <= ('0' & UNSIGNED(A)) + ('0' & UNSIGNED(B));
                RES  <= STD_LOGIC_VECTOR(
                            UNSIGNED(A) + UNSIGNED(B)
                        );

            -- Subtraction
            when "001" =>
                RES <= STD_LOGIC_VECTOR(
                           UNSIGNED(A) - UNSIGNED(B)
                       );

            -- Bitwise AND
            when "010" =>
                RES <= A AND B;

            -- Bitwise OR
            when "011" =>
                RES <= A OR B;

            -- Bitwise XOR
            when "100" =>
                RES <= A XOR B;

            -- Default
            when others =>
                RES <= (others => '0');

        end case;
    end process;

    RESULT <= RES;

    CARRY_OUT <= TEMP(8) when SEL = "000" else '0';

    ZERO <= '1' when RES = "00000000" else '0';

end Behavioral;