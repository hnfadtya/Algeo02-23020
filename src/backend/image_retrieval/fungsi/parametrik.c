import java.util.Scanner;

public class GaussJordanElimination {
    public static String driverGaussJordanElimination(){
        double[][] matrix = new double[0][0];
        @SuppressWarnings("resource")
        Scanner scanner = new Scanner(System.in);
        while (true){
            System.out.print("Ambil variabel dari file?(Y/n/C) : ");
            try{char choice = BasicFunction.readInput().charAt(0);
            if (choice == 'Y' || choice == 'y'){
                System.out.print("Masukan path ke file (D:/Documents/var.txt): ");
                String filename = scanner.nextLine();
                matrix = InputOutput.readMatrixFile(filename);
                break;
            } else if (choice == 'N' || choice == 'n'){
                matrix = BasicFunction.inputMatrix();
                break;
            } else if (choice == 'C' || choice == 'c'){
                return "0.267";
            } else {
                System.out.println("Masukan tidak valid.");
            }
            } catch (Exception e){
                System.out.println("Error, silahkan coba lagi.");
            }
        }
        String hasil = gaussJordanElimination(matrix);
        if (hasil == null){return "0.267";}
        else {return hasil;}
    }
    public static String readInput() throws Exception {
        StringBuilder inputBuilder = new StringBuilder();
        int character;
        while ((character = System.in.read()) != '\n') {
            inputBuilder.append((char) character);
        }
        return inputBuilder.toString();
    }

    public static String gaussJordanElimination(double[][] matrix) {
        int n = matrix.length;
        int m = matrix[0].length;
        boolean hasFreeVariable = false;
        int idxPivot = 0;
        
        for (int i = 0; i < n; i++) {
            while (idxPivot < m - 1 && Math.abs(matrix[i][idxPivot]) < 1e-9) {
                if (!switchRow(matrix, i)) {
                    hasFreeVariable = true; // Jika terdapat solusi banyak maka penukaran pivot akan dilewati dan ditandai solusi parametrik
                    idxPivot++;
                    if (idxPivot == m - 2) break;
                }
            }
            
            if (idxPivot == m - 2) break; // Mencegah akses indekx kolumn di luar batasan 
            
            // Normalisasi pivot
            double pivot = matrix[i][idxPivot];
            if (Math.abs(pivot) > 1e-9){
                for(int k = idxPivot; k < m; k++){
                    matrix[i][k] /= pivot;
                }
            }

            // Eliminasi Gauss (Baris bawah)
            for (int j = i + 1; j < n; j++) {
                if (Math.abs(matrix[j][idxPivot]) > 1e-9) {
                    double factor = matrix[j][idxPivot] / matrix[i][idxPivot];
                    for (int k = idxPivot; k < m; k++) {
                        matrix[j][k] -= factor * matrix[i][k];
                    } 
                }

            }

            // Eliminasi Gauss (Baris atas)
            for(int j = i -1 ; j>= 0; j--){
                if(Math.abs(matrix[j][idxPivot]) > 1e-9){ // Jika element di atas baris pivot bukan nol maka dimasukkan nilainya dalam faktor
                    double factor  = matrix[j][idxPivot];
                    for (int k = idxPivot; k < m; k++){
                        matrix[j][k] -= factor * matrix[i][k];
                    }
                }
            }

            idxPivot ++;
        }
        
        // Cek apakah ada baris nol dan augmented kolom juga nol (solusi banyak)
        for (int i = 0; i < n; i++) {
            if (isRowZero(matrix[i]) && Math.abs(matrix[i][m-1]) < 1e-9) {
                hasFreeVariable = true;
            }
            // Cek apakah terdapat baris nol dan nilai di kolom augmented tidak nol (tidak ada solusi)
            if (isRowZero(matrix[i]) && Math.abs(matrix[i][m-1]) > 1e-9) {
                System.err.println("Tidak ditemukan solusi unik");
                return null;
            }
        }
        System.out.println("\nMatrix akhir:");
        BasicFunction.printMatrix(matrix);
        if (hasFreeVariable){
            System.err.println("Ditemukan solusi parametric");
            return GaussElimination.parametricBackSubstitution(matrix);
        }        
        else{
            return GaussElimination.printNormalBackSubstitution(GaussElimination.normalBackSubstitution(matrix));
        }
    }

    // Memeriksa apakah sebuah baris adalah baris nol
    public static boolean isRowZero(double[] row) {
        for (int i = 0; i < row.length - 1; i++) { 
            if (row[i] != 0) {
                return false;
            }
        }
        return true;
    }

    // Mengubah baris jika elemen diagonal adalah nol
    public static boolean switchRow(double[][] matrix, int i) {
        for (int row = i + 1; row < matrix.length; row++) {
            if (matrix[row][i] != 0) {
                for (int j = 0; j < matrix[i].length; j++) {
                    double temp = matrix[i][j];
                    matrix[i][j] = matrix[row][j];
                    matrix[row][j] = temp;
                }
                return true; 
            }
        }
        return false; // Tidak ada baris yang bisa ditukar
    }
    public static void printArrayJordan(double[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            System.out.printf("x%d = %.4f\n", i + 1, matrix[i][matrix[i].length - 1]);
        }
    }
}