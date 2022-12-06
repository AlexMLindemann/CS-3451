    # for i in vTable: #loop over all verts in vTable O(n^2)
    #     for j in vTable:
    #         if vTable[nextCorner(i)] == vTable[prevCorner(j)] and vTable[prevCorner(i)] == vTable[nextCorner(j)]:
    #             opTable[i] = j
    #             opTable[j] = i
    # return opTable

    tripDict = {}
    for i, triplet in enumerate(triplets):
        if tuple(triplet) not in tripDict:
            tripDict[tuple(triplet)] = i
    print(tripDict)

    # Iterate over the elements in the array
    for i, triplet in enumerate(triplets):
        # Use the zip function to create pairs of triplets`   `
        pairs = zip(triplets[i:], triplets[i + 1:])
        # Iterate over the pairs of triplets
        for pair in pairs:
            # Use the pairs as keys in the dictionary to fill out the opposite
            cornerA = pair[0]
            cornerB = pair[1]
            opTable[tuple(tripDict[cornerA])] = cornerB
        return opTable

    for i in range(0, len(sortedTriplets) - 1, 1):
        cornerA = sortedTriplets[i][2]
        print "cornerA: ", cornerA
        cornerB = sortedTriplets[i+1][2]
        print "cornerB: ", cornerB
        # opTable = {
        #     vTable[cornerA]: cornerB,
        #     vTable[cornerB]: cornerB
        #     }
        # print "opTable: " + str(opTable)

        opTable[sortedTriplets[i][2]] = vTable[sortedTriplets[i+1][2]]
        opTable[sortedTriplets[i+1][2]] = vTable[sortedTriplets[i][2]]
    return opTable 