subroutine add_arrays(a, b, c, n)
    implicit none
    integer, intent(in) :: n
    real(8), intent(in) :: a(n), b(n)
    real(8), intent(out) :: c(n)
    integer :: i
    
    do i = 1, n
        c(i) = a(i) + b(i)
    end do
end subroutine add_arrays