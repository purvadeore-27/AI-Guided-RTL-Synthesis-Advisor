library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ripple_carry_adder is
    Port (
        A    : in  STD_LOGIC_VECTOR(3 downto 0);
        B    : in  STD_LOGIC_VECTOR(3 downto 0);
        Cin  : in  STD_LOGIC;
        SUM  : out STD_LOGIC_VECTOR(3 downto 0);
        Cout : out STD_LOGIC
    );
end ripple_carry_adder;

architecture Behavioral of ripple_carry_adder is

    signal C : STD_LOGIC_VECTOR(4 downto 0);

begin

    C(0) <= Cin;

    SUM(0) <= A(0) XOR B(0) XOR C(0);
    C(1) <= (A(0) AND B(0)) OR
            (A(0) AND C(0)) OR
            (B(0) AND C(0));

    SUM(1) <= A(1) XOR B(1) XOR C(1);
    C(2) <= (A(1) AND B(1)) OR
            (A(1) AND C(1)) OR
            (B(1) AND C(1));

    SUM(2) <= A(2) XOR B(2) XOR C(2);
    C(3) <= (A(2) AND B(2)) OR
            (A(2) AND C(2)) OR
            (B(2) AND C(2));

    SUM(3) <= A(3) XOR B(3) XOR C(3);
    C(4) <= (A(3) AND B(3)) OR
            (A(3) AND C(3)) OR
            (B(3) AND C(3));

    Cout <= C(4);

end Behavioral;