library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_half_adder is
end tb_half_adder;

architecture Behavioral of tb_half_adder is

    signal A     : STD_LOGIC := '0';
    signal B     : STD_LOGIC := '0';
    signal SUM   : STD_LOGIC;
    signal CARRY : STD_LOGIC;

begin

    uut: entity work.half_adder
        port map (
            A     => A,
            B     => B,
            SUM   => SUM,
            CARRY => CARRY
        );

    process
    begin

        -- Test 00
        A <= '0';
        B <= '0';
        wait for 10 ns;

        assert SUM = '0' and CARRY = '0'
            report "Test 00 failed"
            severity error;

        -- Test 01
        A <= '0';
        B <= '1';
        wait for 10 ns;

        assert SUM = '1' and CARRY = '0'
            report "Test 01 failed"
            severity error;

        -- Test 10
        A <= '1';
        B <= '0';
        wait for 10 ns;

        assert SUM = '1' and CARRY = '0'
            report "Test 10 failed"
            severity error;

        -- Test 11
        A <= '1';
        B <= '1';
        wait for 10 ns;

        assert SUM = '0' and CARRY = '1'
            report "Test 11 failed"
            severity error;

        report "HALF ADDER TEST PASSED"
            severity note;

        wait;

    end process;

end Behavioral;